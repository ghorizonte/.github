"""Regression tests for the organization onboarding required workflow (no GitHub access)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from corporate_onboarding_gate import (  # noqa: E402
    AUTHORITY, MARKER_START, MARKER_END, REQUIRED, check_owners
)


def compliant():
    footer = "\n".join(f"{name} {AUTHORITY}" for name in sorted(REQUIRED))
    return (
        "* @ghorizonte/tech-leads @ghorizonte/risk-reviewers\n"
        "/src/** @ghorizonte/tech-leads\n\n"
        + MARKER_START + "\n" + footer + "\n" + MARKER_END + "\n"
    )


class CorporateOnboardingGateTests(unittest.TestCase):
    def test_expected_corporate_file_passes(self):
        self.assertEqual(check_owners("ghorizonte/robo", compliant()), [])

    def test_missing_file_fails(self):
        self.assertIn("CODEOWNERS_MISSING", check_owners("ghorizonte/robo", ""))

    def test_missing_critical_path_fails(self):
        content = compliant().replace("/AGENTS.md @edsoness-hub\n", "")
        self.assertIn("MISSING_PROTECTED_PATH:/AGENTS.md", check_owners("ghorizonte/robo", content))

    def test_non_authoritative_footer_fails(self):
        content = compliant() + "\n/AGENTS.md @ghorizonte/developers\n"
        self.assertIn("CORPORATE_FOOTER_NOT_AUTHORITATIVE", check_owners("ghorizonte/robo", content))

    def test_other_owner_in_footer_fails(self):
        content = compliant().replace("/AGENTS.md @edsoness-hub", "/AGENTS.md @ghorizonte/developers")
        reasons = check_owners("ghorizonte/robo", content)
        self.assertIn("UNEXPECTED_CORPORATE_OWNER_RULE", reasons)
        self.assertIn("MISSING_PROTECTED_PATH:/AGENTS.md", reasons)

    def test_no_risk_reviewers_fails(self):
        content = compliant().replace(" @ghorizonte/risk-reviewers", "")
        self.assertIn("OPERATIONAL_RISK_REVIEWER_MISSING", check_owners("ghorizonte/robo", content))

    def test_duplicate_marker_fails(self):
        self.assertIn("CORPORATE_FOOTER_MISSING_OR_AMBIGUOUS", check_owners(
            "ghorizonte/robo", compliant() + MARKER_START))

    def test_governance_repository_does_not_need_generic_footer(self):
        self.assertEqual(check_owners("ghorizonte/.github",
                                      "* @ghorizonte/tech-leads\n/.github/CODEOWNERS @edsoness-hub\n"), [])
        self.assertEqual(check_owners("ghorizonte/gh-automation",
                                      "* @ghorizonte/tech-leads\n/.github/CODEOWNERS @edsoness-hub\n"), [])

    def test_governance_repository_needs_authority(self):
        self.assertIn("GOVERNANCE_CODEOWNERS_AUTHORITY_MISSING",
                      check_owners("ghorizonte/repo-template-corporativo", "* @ghorizonte/tech-leads\n"))

    def test_other_organization_rejected(self):
        self.assertEqual(check_owners("other/robo", compliant()), ["INVALID_REPOSITORY"])


if __name__ == "__main__":
    unittest.main()
