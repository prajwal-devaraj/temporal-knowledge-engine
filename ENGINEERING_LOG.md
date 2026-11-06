# Engineering log — November 5–9, 2026

This log is meant to record work actually completed, with command outputs, commit IDs, and decisions. Entries for future dates are prompts, not claims of completed work.

## November 5 — Review and problem framing

Status: **Fill in after checking your own notes/history.**

- What requirements did I read?
- Which five snapshot dates and product categories did I investigate?
- What mistakes did I notice in the starter implementation?
- Any screenshots, command output, or notes worth linking?

## November 6 — Working baseline

A local implementation and evaluation are available. Verify the exact commands on your computer before committing this entry as your own run.

- Implementation: separate dated indexes, passage retrieval, structured table handling, source ranking, and a conflict inventory.
- Practice scorer: 40 questions; QA 0.8667; zero execution errors.
- Consistency: repeated and paraphrased questions scored 1.0 in the local report.
- Speed: reported p95 latency 0.33 seconds.
- Areas to revisit: branch details, multi-item completeness, and cross-page conflicts.
- My own observations / changes: **[add after reviewing and rerunning]**
- Commit: **[add actual hash]**

## November 7 — Source authority and history

Status: **Planned; write results only after doing the work.**

- Inspect specific old-vs-new rate disagreements.
- Test authoritative rates pages against stale calculators.
- Check behavior for dates between crawls and dates before the first crawl.
- Record the score before/after the changes and the commit.

## November 8 — Edge cases and cleanup

Status: **Planned; write results only after doing the work.**

- Check branch address and lobby versus drive-through hours.
- Review multi-product list questions and refusal cases.
- Add focused regression tests for previously missed questions.
- Record failed cases, fixes, and the commit.

## November 9 — Release check

Status: **Planned; write results only after doing the work.**

- Run scorer from a clean environment.
- Check the repository for snapshots, evaluation files, keys, and accidental archives.
- Confirm README instructions, dependencies, and exact commit SHA.
- Record final public score and submit only after reviewing the code yourself.

## Decision notes

For each substantive revision, capture: **problem -> evidence -> decision -> trade-off -> test result**. That provides more useful engineering evidence than an unexplained score or a polished timeline.
