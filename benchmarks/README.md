# Benchmark format

Version 0.1 measures protocol compliance and stability, not abstract creativity.

Each case should contain a problem statement, allowed evidence, hidden evaluation notes, acceptable contradictions, invariants, forbidden unsupported claims, scoring rubric, and expert-review status.

Recommended measures:

- evidence attribution precision;
- contradiction-identification agreement;
- solution-mechanism diversity;
- invariant-violation rate;
- unsupported-claim rate;
- repeat-run stability;
- expert usefulness rating.

For recall or completeness, freeze the expected dependency set independently of the run being scored. If that is unavailable, label the result as recall against a reconstructed known set. Include cases where an immutable release artifact and an intentionally edited working copy have different hashes; a correct run must not infer corruption or recommend replacement without further evidence and authorization.

Do not label a benchmark “expert validated” until named reviewers approve its cases and rubric.
