# Implementation notes

## Main idea

I treat each website crawl as a dated collection of evidence rather than merging all pages into one source of truth. During `ingest`, the system creates a separate passage index for each snapshot and remembers rate-table rows for later comparison. `answer` chooses the right snapshot first, retrieves relevant passages, then selects evidence with attention to source type and question qualifiers. `conflicts` reports changes it can identify in comparable structured rate rows.

## Why this design

The assignment has two different problems: finding relevant information and deciding whether that information applies. A broad keyword match can retrieve a rate but miss its loan term, balance tier, or date. The implementation indexes Markdown table rows with their headers, keeps old snapshots available, and boosts official product/rate pages relative to calculators or archive content. A question with an `as_of` date can only consult a snapshot taken on or before that date. The goal is to make a specific, defensible choice rather than repeat several disagreeing numbers.

I used a deterministic local approach instead of a hosted language model. That removes API-key setup, keeps the scoring run offline, and gives consistent repeated answers. It also has clear limits: complex wording and pages with unusual formatting are harder to interpret without richer semantic parsing.

## What I tested

The participant-kit scorer was run locally against its 40 public questions on November 6, 2026. The latest recorded result was 0.8667 QA score, 0 runner errors, 0 stale-trap hits, and repeat/paraphrase consistency of 1.0. The scorer reported p95 answer latency of 0.33 seconds. These numbers describe that local test only; the hidden evaluation can differ. Conflict-detection accuracy cannot be inferred from the available summary alone.

## Known limitations and next improvements

- Branch information: improve address/hours matching so the right branch and lobby/drive-through distinction are preserved.
- Conflict resolution: compare facts across differently structured pages, not only recurring rate-table rows.
- List questions: improve completeness without including unrelated products or stale values.
- Extraction: handle more Markdown layouts and strengthen confidence thresholds for ambiguous evidence.

## Reproduce

From the extracted participant kit root, with this folder named `submission`:

```bash
python harness/run_eval.py --submission submission --eval eval/public_eval.jsonl
```

The submission uses Python 3.11 standard-library modules only. **No API keys, paid APIs, or live website calls are needed.** The supplied snapshots and evaluation assets must remain outside the public repository.
