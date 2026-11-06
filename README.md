# Credit union knowledge system

A Python implementation of the interface.ai knowledge-system exercise. The system searches five dated website snapshots, returns a cited answer when it has enough evidence, and keeps track of changed rates across snapshots.

## What I chose to build

I kept the answer path local and deterministic. Each website download is indexed separately so an `as_of` question does not accidentally use information that appeared later. For rate questions, I try to match the product and the relevant table row before choosing a value. I also rank official product pages ahead of older calculators and archived articles when the pages disagree.

This is intentionally not a general-purpose chatbot. The trade-off is less natural-language flexibility in exchange for reproducible results, low response times, and no external dependencies.

## Files

- `solution.py`: implementation of `build()`, `ingest()`, `answer()`, and `conflicts()`
- `requirements.txt`: no third-party packages required
- `NOTES.md`: technical decisions, limitations, and reproduction steps
- `ENGINEERING_LOG.md`: dated work log to fill in with actual changes and test outcomes

## Run it

Python 3.11 is recommended. Use the participant kit provided for the assignment; the snapshot files and scoring harness are deliberately not part of this repository.

Place this submission folder in the extracted participant kit as `submission/` and run the following from the kit root:

```bash
python harness/run_eval.py --submission submission --eval eval/public_eval.jsonl
```

The evaluation uses the same three-method contract as the supplied starter. No API credentials or network access are needed.

## Public practice baseline

The current local baseline on the 40 supplied practice questions is **0.8667** (November 6, 2026), with zero runner errors. The score is a practice result, not a prediction of the private evaluation. Weak spots include branch information, conflict resolution, and complete list questions.

## Data handling

The employer's website snapshots, participant kit, evaluation files, and secrets are intentionally excluded from the public repository. Do not upload them.
