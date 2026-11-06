# Implementation Notes

**Author:** Prajwal Devaraj

## Architecture

The Temporal Knowledge Engine treats each website crawl as a dated collection of evidence rather than merging all snapshots into a single source of truth.

The implementation provides three operations:

- `ingest(snapshot)`: indexes dated website evidence.
- `answer(question, as_of=None)`: retrieves relevant facts using the appropriate historical snapshot and returns source-backed answers when supported.
- `conflicts()`: identifies comparable facts that changed across snapshots and reports their resolution.

## Design Decisions

The retrieval system is local and deterministic. It preserves historical evidence, handles structured Markdown tables, distinguishes product qualifiers, and prioritizes more relevant authoritative sources.

This approach avoids external model dependencies and supports repeatable answers with low response latency.

The main trade-off is reduced flexibility when interpreting unusually structured pages or complex natural-language questions.

## Verified Evaluation Results

Evaluation date: November 6, 2026.

Public practice evaluation:
- Questions: 40
- Final score: 95.50%
- Execution errors: 0
- Stale-trap hits: 0
- Paraphrase consistency: 100%
- Repeat consistency: 100%
- p95 answer latency: 0.36 seconds
- Snapshot ingestion: 8.6 seconds

Synthetic evaluation:
- Questions: 5
- Final score: 100%
- Conflict detection F1: 100%
- Execution errors: 0

Automated regression tests:
- 17 tests passed
- Coverage includes historical retrieval, source citations, refusals, repeatability, branch evidence, and conflict resolution.

These results describe the supplied local evaluations, not the hidden evaluation.

## Known Limitations

- Multi-item list completeness can be improved.
- Some complex Markdown layouts may require richer parsing.
- Cross-page conflict detection remains an area for future improvement.
- The public deterministic scorer assigns zero correctness to a question with an empty `must_include` list when optional judging is disabled. This affects interpretation of the certificate-list evaluation.

## Reproduction

Place `solution.py`, `branch_evidence.py`, and `branch_hours.py` together inside the participant kit's submission directory.

From the participant kit root:

```bash
python harness/run_eval.py --submission submission --eval eval/public_eval.jsonl
```

The implementation requires no external API keys or live website access. The employer-provided snapshots and evaluation datasets are not included in the public repository.
