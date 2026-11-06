# Engineering Log

**Author:** Prajwal Devaraj

## November 5, 2026 — Problem Review and Initial Development

### Requirements and Problem Understanding

Reviewed the temporal knowledge-system assignment and its evaluation requirements, including historical questions, source citations, conflict resolution, qualified financial rates, and refusal behavior.

Examined the provided snapshot-based evaluation workflow and identified the importance of preserving historical evidence instead of relying exclusively on the latest crawled content.

### Initial Engineering Direction

Established the direction for a local, deterministic retrieval system designed to support source-backed answers, historical queries, and repeatable evaluation.

The implementation and testing work continued on November 6.

## November 6, 2026 — Implementation and Validation

### System Design

Implemented a temporal knowledge retrieval system for website snapshots, preserving dated evidence rather than overwriting historical facts.

The solution includes:
- Snapshot-aware ingestion and retrieval
- Historical `as_of` question handling
- Structured rate-table extraction
- Source ranking and citations
- Conflict detection and resolution
- Refusal when sufficient evidence is unavailable

### Evidence Extraction

Improved handling of dated branch-count evidence and branch-specific lobby and drive-up hours.

Separated these capabilities into supporting modules:
- `branch_evidence.py`
- `branch_hours.py`

### Regression Testing

Added unit and integration tests covering:
- Publication-date extraction
- Historical evidence isolation
- Branch-count selection
- Branch-hours extraction
- Current and historical certificate rates
- Citation validity against source documents
- Unsupported-question refusal
- Paraphrase and repeated-answer consistency
- Certificate-rate conflict detection

Final automated test result: 17/17 passed.

### Evaluation

Verified the implementation using the supplied evaluation harness.

Public practice evaluation:
- 40 questions
- Final score: 95.50%
- Zero execution errors
- Zero stale-trap hits
- 100% paraphrase and repeat consistency
- p95 answer latency: 0.36 seconds
- Ingestion time: 8.6 seconds

Synthetic evaluation:
- 5 questions
- Final score: 100%
- Conflict detection F1: 100%
- Zero execution errors

### Investigation: Certificate List Completeness

Investigated the broad certificate-rate question `dup-005`.

The public test has an empty `must_include` list. The deterministic scorer assigns correctness 0.0 to such questions when optional LLM judging is disabled.

Alternative implementations were evaluated, but they did not improve the verified overall public score.

Decision:
- Preserve the 95.50% implementation.
- Do not modify the evaluation harness.
- Document list completeness as a known limitation.
- Protect historical rate selection and refusal behavior from regressions.

### Submission Rehearsal

Copied the three production modules into an isolated submission directory and ran the supplied evaluations successfully.

The isolated rehearsal reproduced:
- 95.50% public evaluation
- 100% synthetic evaluation
- Zero runner errors

### Engineering Trade-offs

The system prioritizes temporal correctness, reproducibility, source traceability, and fast local execution over unrestricted natural-language generation.

The public evaluation is a practice benchmark. Hidden evaluation results may differ.
