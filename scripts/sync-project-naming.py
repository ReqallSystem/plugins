#!/usr/bin/env python3
"""Copy the built canonical policy, or check that vendored copies match it.

Run `npm run build` in ../core first. No network or installed-profile access.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def sources_and_targets(workspace: Path):
    source = workspace / "core/src/project-policy.ts"
    built = workspace / "core/dist/project-policy.js"
    ts = source.read_bytes()
    # A vendored .mjs must not point at core's unshipped source map.
    js = re.sub(rb"(?m)^//# sourceMappingURL=.*\n?", b"", built.read_bytes())
    return [
        (workspace / "claude-plugin/src/hooks/project-policy.ts", ts),
        (workspace / "pi-plugin/extensions/project-policy.ts", ts),
        (workspace / "cursor-plugin/src/project-policy.ts", ts),
        (workspace / "codex-plugin/scripts/lib/project-policy.mjs", js),
        (workspace / "grok-plugin/scripts/lib/project-policy.mjs", js),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--check", action="store_true", help="read-only drift check")
    args = parser.parse_args()
    failures = []
    for path, expected in sources_and_targets(args.workspace.resolve()):
        if args.check:
            if not path.is_file() or path.read_bytes() != expected:
                failures.append(str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
            print(f"Updated {path}")
    if failures:
        for path in failures:
            print(f"DRIFT: {path}")
        return 1
    print("All five vendored policies match core." if args.check else "Synced five policy copies; rebuild TypeScript consumers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
