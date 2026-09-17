"""Offline contract checks for the SLEEP skills in sibling repositories.

Run from this repository: python -B -m unittest discover -s test -p 'test_sleep_guidance.py' -v
These check shipped instructions, not model judgment or live SLEEP execution.
"""
from pathlib import Path
import unittest


WORKSPACE = Path(__file__).resolve().parents[2]
CANONICAL = WORKSPACE / "reqall_net/doc/SLEEP.md"
SKILLS = {
    "claude-plugin": "skills/sleep/SKILL.md",
    "codex-plugin": "skills/sleep/SKILL.md",
    "hermes-plugin": "skills/sleep/SKILL.md",
    "grok-plugin": "skills/sleep/SKILL.md",
    "grok-bot-plugin": "skills/reqall-sleep/SKILL.md",
    "pi-plugin": "skills/reqall-sleep/SKILL.md",
}
HEADING = "## WORK review policy"
REQUIRED = (
    "get_record", "list_links", "search", "ARCH/SPEC",
    "Alignment is not redundancy", "regression fixes", "test evidence",
    "no unique durable information", "useful relationships",
    "linked `issue`", "Do not automatically rewrite ARCH/SPEC",
    "Missing links do not prove new requirements", "confirmed requirements",
    "Leave ambiguous cases unchanged", "historical qualifications",
    "Never replay a destructive batch",
)


def policy(text):
    if text.count(HEADING) != 1:
        raise AssertionError("Expected exactly one WORK review policy section")
    return text.split(HEADING + "\n", 1)[1].split("\n## ", 1)[0].strip()


class SleepGuidanceTests(unittest.TestCase):
    def test_canonical_policy_covers_judgment_and_verification(self):
        block = policy(CANONICAL.read_text())
        for phrase in REQUIRED:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, block)

    def test_six_shipped_skills_match_canonical_policy(self):
        canonical = policy(CANONICAL.read_text())
        for repo, relative in SKILLS.items():
            with self.subTest(repo=repo):
                text = (WORKSPACE / repo / relative).read_text()
                self.assertEqual(policy(text), canonical)
                self.assertIn("`work_review`", text)
                self.assertIn("**promote**", text)
                self.assertIn("**discard**", text)
                self.assertIn("no unique durable information", text)
                self.assertNotIn("graph is healthy", text)
                self.assertNotIn("graph healthy", text)

    def test_judgment_examples_are_documented_not_live_test_claims(self):
        text = CANONICAL.read_text()
        for case in (
            "Aligned, redundant", "Aligned, new evidence", "Implementation deviation",
            "Possible spec defect", "Unlinked, existing intent", "Unlinked, novel fact",
            "Ambiguous or inaccessible",
        ):
            with self.subTest(case=case):
                self.assertIn(case, text)
        self.assertIn("illustrative judgment cases, not live-run coverage", text)

    def test_claude_allowed_tools_include_readback_and_linking(self):
        text = (WORKSPACE / "claude-plugin" / SKILLS["claude-plugin"]).read_text()
        frontmatter = text.split("---", 2)[1]
        for prefix in ("mcp__plugin_reqall_reqall__", "mcp__Reqall__"):
            for op in ("get_record", "list_records", "list_links", "search", "upsert_link"):
                with self.subTest(prefix=prefix, op=op):
                    self.assertIn(prefix + op, frontmatter)


if __name__ == "__main__":
    unittest.main()
