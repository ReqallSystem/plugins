#!/usr/bin/env python3
"""Exercise identical temporary project trees across Reqall sibling checkouts.

Prerequisites: build core, Claude and Cursor; install their dev dependencies.
Pi's TypeScript policy requires Node's type stripping (Node 22.18+).
No real HOME, credentials, installed profiles, network, or MCP writes are used.
"""
from __future__ import annotations

import argparse
from collections import Counter
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def run(command, **kwargs):
    return subprocess.run(command, check=True, capture_output=True, text=True, timeout=120, **kwargs)


def child_path(root: Path, relative: str) -> Path:
    candidate = root / relative
    if candidate.resolve().is_relative_to(root.resolve()):
        return candidate
    raise ValueError(f"Fixture path escapes temporary tree: {relative!r}")


def prepare(parent: Path, case: dict) -> dict:
    root = parent / case["id"]
    root.mkdir()
    cwd = child_path(root, case.get("cwd", "."))
    cwd.mkdir(parents=True, exist_ok=True)
    home = root / "isolated-home"
    home.mkdir()
    env = {
        "PATH": os.environ.get("PATH", os.defpath),
        "HOME": str(home),
        "HERMES_HOME": str(home / ".hermes"),
        "CLAUDE_PLUGIN_DATA": str(home / "claude-state"),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "REQALL_MACHINE_NAME": "CONTRACT.HOST",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
    }
    env.update({k: v.replace("$root", str(root)) for k, v in case.get("env", {}).items()})
    if case.get("marker", True):
        (root / ".reqall-workspace").touch()
    for directory in case.get("directories", []):
        child_path(root, directory).mkdir(parents=True, exist_ok=True)
    files = {key: value.encode("utf8") for key, value in case.get("files", {}).items()}
    files.update({key: bytes(value) for key, value in case.get("binary_files", {}).items()})
    files.update({key: (value[0] * value[1]).encode("utf8") for key, value in case.get("repeat_files", {}).items()})
    for name, data in files.items():
        target = child_path(root, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    # Targets are relative to the fixture root, not the link's parent. Both
    # endpoints stay in the temporary tree, even for workspace-boundary escapes.
    for name, target in case.get("symlinks", {}).items():
        link = child_path(root, name)
        destination = child_path(root, target)
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(destination)
    # A real local repository tests the exact argv-based origin lookup, without
    # connecting to remotes. Empty template suppresses user-supplied Git hooks.
    run(["git", "init", "--quiet", "--template=", str(root)], env=env)
    if case.get("remote"):
        run(["git", "remote", "add", "origin", case["remote"]], cwd=root, env=env)
    return {**case, "cwd": str(cwd), "env": env, "prompt": case.get("prompt", "")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--report", type=Path)
    parser.add_argument("--policies-only", action="store_true")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    plugin_root = Path(__file__).resolve().parents[1]
    fixtures = json.loads((plugin_root / "test/project-naming-cases.json").read_text())["cases"]
    assert len({c["id"] for c in fixtures}) == len(fixtures), "Duplicate fixture IDs"
    # Check Python and vendored policy source drift before exercising any code.
    run([sys.executable, str(plugin_root / "scripts/sync-project-naming.py"), "--workspace", str(workspace), "--check"])
    with tempfile.TemporaryDirectory(prefix="reqall-project-contract-") as tmp:
        cases = [prepare(Path(tmp), c) for c in fixtures]
        baseline_env = dict(os.environ)
        os.environ.clear()
        os.environ.update(cases[0]["env"])
        sys.path.insert(0, str(workspace / "hermes-plugin"))
        project = importlib.import_module("reqall.project")
        results = []
        for case in cases:
            os.environ.clear()
            os.environ.update(case["env"])
            try:
                binding = project.bind_project(cwd=case["cwd"], env=None if case.get("use_default_env") else case["env"], prompt=case["prompt"])
                results.append({"host": "hermes", "id": case["id"], "name": binding.name, "source": binding.source})
            except Exception as error:
                results.append({"host": "hermes", "id": case["id"], "error": repr(error)})
        payload = {"workspace": str(workspace), "cases": cases, "policiesOnly": args.policies_only}
        js = run(["node", str(plugin_root / "scripts/project-naming-bridge.mjs")], input=json.dumps(payload), env=cases[0]["env"])
        results.extend(json.loads(js.stdout))
        expected_machine = project.machine_project_name(cases[0]["env"])
        os.environ.clear()
        os.environ.update(baseline_env)
    by_id = {c["id"]: c for c in fixtures}
    expected_hosts = {"hermes", "core", "claude", "codex", "grok", "pi", "cursor", "cline", "opencode", "openclaw"}
    if not args.policies_only:
        expected_hosts.update({"core-public", "claude-public", "codex-public", "grok-public", "cursor-public"})
    expected_pairs = {(host, case["id"]) for host in expected_hosts for case in fixtures}
    actual_pairs = [(r["host"], r["id"]) for r in results]
    assert len(actual_pairs) == len(set(actual_pairs)), "Duplicate results"
    assert set(actual_pairs) == expected_pairs, "Missing/unexpected runtime coverage"
    failures = []
    for result in results:
        case = by_id[result["id"]]
        expected = expected_machine if case["expected"] == "$machine" else case["expected"].replace("$user", expected_machine.rsplit("/", 1)[1])
        if result.get("name") != expected or (not result["host"].endswith("-public") and result.get("source") != case["source"]):
            failures.append({**result, "expected": expected, "expected_source": case["source"]})
    report = {
        "fixture_count": len(fixtures),
        "runtime_count": len(expected_hosts),
        "check_count": len(results),
        "passed": len(results) - len(failures),
        "failed": len(failures),
        "per_runtime": dict(sorted(Counter(r["host"] for r in results).items())),
        "failures": failures,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
