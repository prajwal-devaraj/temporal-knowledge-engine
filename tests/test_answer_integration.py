"""Integration tests against the supplied interface.ai synthetic snapshots."""

import os
import sys
import unittest
from pathlib import Path

DEFAULT_KIT = (
    "/tmp/interface-ai-evaluation/"
    "hackathon-knowledge-kit-participant"
)
KIT = Path(
    os.environ.get("INTERFACE_AI_KIT", DEFAULT_KIT)
).expanduser().resolve()

if str(KIT) not in sys.path:
    sys.path.insert(0, str(KIT))

from harness.run_eval import load_snapshots, to_answer
import solution


class AnswerIntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.snapshots = load_snapshots(
            KIT / "harness/selftest/snapshots"
        )
        cls.engine = solution.build()

        for snapshot in cls.snapshots:
            cls.engine.ingest(snapshot)

        cls.pages_by_snapshot = {
            snapshot.snapshot_id: {
                page.url: page.markdown
                for page in snapshot.pages
            }
            for snapshot in cls.snapshots
        }

    def ask(self, question, as_of=None):
        return to_answer(
            self.engine.answer(question, as_of)
        )

    def test_current_certificate_rate(self):
        answer = self.ask("What is the 6-month certificate APY?")

        self.assertTrue(answer.confident)
        self.assertIn("3.50%", answer.text)
        self.assertNotIn("2.95%", answer.text)

    def test_historical_certificate_rate(self):
        answer = self.ask(
            "What was the 6-month certificate APY in January 2026?",
            "2026-01-31",
        )

        self.assertTrue(answer.confident)
        self.assertIn("2.95%", answer.text)
        self.assertNotIn("3.50%", answer.text)

    def test_historical_source_is_not_future_snapshot(self):
        answer = self.ask(
            "What was the 6-month certificate APY in January 2026?",
            "2026-01-31",
        )

        self.assertTrue(answer.sources)

        for source in answer.sources:
            self.assertEqual(
                source.snapshot_id,
                "01_2026-01-05_baseline",
            )

    def test_current_rate_uses_updated_snapshot(self):
        answer = self.ask("What is the 6-month certificate APY?")

        self.assertTrue(answer.sources)
        self.assertTrue(
            any(
                source.snapshot_id == "02_2026-03-01_update"
                for source in answer.sources
            )
        )

    def test_debit_card_replacement_fee(self):
        answer = self.ask(
            "How much is a lost debit card replacement?"
        )

        self.assertTrue(answer.confident)
        self.assertIn("$2.50", answer.text)
        self.assertTrue(answer.sources)

    def test_unknown_rate_requires_refusal(self):
        answer = self.ask(
            "What is the 60-month jumbo certificate rate?"
        )

        self.assertFalse(answer.confident)
        self.assertNotIn("3.50%", answer.text)
        self.assertNotIn("2.95%", answer.text)

    def test_sources_reference_real_snapshot_content(self):
        questions = [
            ("What is the 6-month certificate APY?", None),
            (
                "What was the 6-month certificate APY in January 2026?",
                "2026-01-31",
            ),
            ("How much is a lost debit card replacement?", None),
        ]

        for question, as_of in questions:
            with self.subTest(question=question):
                answer = self.ask(question, as_of)
                self.assertTrue(answer.sources)

                for source in answer.sources:
                    self.assertIn(
                        source.snapshot_id,
                        self.pages_by_snapshot,
                    )

                    pages = self.pages_by_snapshot[
                        source.snapshot_id
                    ]

                    self.assertIn(source.url, pages)
                    self.assertTrue(source.quote.strip())
                    self.assertIn(
                        source.quote.strip(),
                        pages[source.url],
                    )

    def test_paraphrased_questions_agree(self):
        first = self.ask(
            "What is the 6-month certificate APY?"
        )
        second = self.ask(
            "Current APY on a six month share certificate?"
        )

        self.assertTrue(first.confident)
        self.assertTrue(second.confident)
        self.assertIn("3.50%", first.text)
        self.assertIn("3.50%", second.text)

    def test_repeated_answers_are_stable(self):
        question = "What is the 6-month certificate APY?"

        answers = [
            self.ask(question)
            for _ in range(5)
        ]

        for answer in answers[1:]:
            self.assertEqual(answer.text, answers[0].text)
            self.assertEqual(
                answer.confident,
                answers[0].confident,
            )
            self.assertEqual(
                answer.sources,
                answers[0].sources,
            )

    def test_certificate_rate_conflict(self):
        conflicts = self.engine.conflicts()

        matching = [
            conflict
            for conflict in conflicts
            if "2.95%" in conflict.values
            and "3.50%" in conflict.values
        ]

        self.assertTrue(
            matching,
            "Expected historical certificate-rate conflict",
        )

        conflict = matching[0]

        self.assertEqual(conflict.resolution, "3.50%")
        self.assertTrue(conflict.sources)
        self.assertTrue(conflict.reason.strip())


if __name__ == "__main__":
    unittest.main()
