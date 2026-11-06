"""Regression tests for evidence extraction edge cases."""

import unittest
from branch_evidence import (
    extract_publication_date,
    branch_count_candidates,
    select_branch_count,
)
from branch_hours import extract_branch_hours


class BranchEvidenceTests(unittest.TestCase):

    def test_publication_date(self):
        text = (
            "# Branch announcement\n"
            "April 06, 2026\n"
            "Dupaco has 22 branch office locations."
        )
        self.assertEqual(
            str(extract_publication_date(text)),
            "2026-04-06"
        )

    def test_branch_count_prefers_newer_claim(self):
        pages = {
            "https://example.com/old": (
                "January 01, 2024\n"
                "Dupaco has 23 branch office locations."
            ),
            "https://example.com/new": (
                "April 06, 2026\n"
                "Dupaco has 22 branch office locations."
            ),
        }
        result = select_branch_count(pages)
        self.assertEqual(result["count"], 22)
        self.assertEqual(
            result["url"], "https://example.com/new"
        )

    def test_historical_branch_count(self):
        pages = {
            "https://example.com/old": (
                "January 01, 2024\n"
                "Dupaco has 23 branch office locations."
            ),
            "https://example.com/new": (
                "April 06, 2026\n"
                "Dupaco has 22 branch office locations."
            ),
        }
        result = select_branch_count(
            pages, as_of="2024-12-31"
        )
        self.assertEqual(result["count"], 23)

    def test_missing_branch_count(self):
        self.assertEqual(
            branch_count_candidates({
                "https://example.com": "No branch count published."
            }),
            []
        )


    def test_future_claim_not_used_for_historical_answer(self):
        pages = {
            "https://example.com/2025": (
                "January 15, 2025\n"
                "Dupaco has 23 branch office locations."
            ),
            "https://example.com/2026": (
                "September 15, 2026\n"
                "Dupaco has 22 branch office locations."
            ),
        }

        result = select_branch_count(
            pages, as_of="2025-12-31"
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["count"], 23)



class BranchHoursTests(unittest.TestCase):

    def test_separate_lobby_and_drive_up(self):
        text = (
            "**Lobby**\n"
            "Monday-Friday: 8:30 a.m.-5:30 p.m.\n"
            "Saturday: 8:30 a.m.-12:30 p.m.\n"
            "**Drive-up**\n"
            "Monday-Friday: 8 a.m.-6 p.m.\n"
            "Sunday: ATM only\n"
            "**ABOUT DUPACO**"
        )
        result = extract_branch_hours(text)
        services = {r["service"] for r in result}
        self.assertEqual(services, {"lobby", "drive-up"})

    def test_inline_section_labels(self):
        text = (
            "**Lobby** Monday-Friday: 9 a.m.-5 p.m.\n"
            "Saturday-Sunday: Closed\n"
            "**Drive-up** Monday-Friday: 8 a.m.-6 p.m.\n"
            "Sunday: ATM only"
        )
        result = extract_branch_hours(text)
        self.assertEqual(len(result), 2)
        self.assertIn("9 a.m.", result[0]["schedule"])
        self.assertIn("8 a.m.", result[1]["schedule"])


if __name__ == "__main__":
    unittest.main()
