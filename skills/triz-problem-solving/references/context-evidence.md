# Context and artifact evidence

Use a progressive context funnel:

1. Read the task, governing instructions, current state, and directly affected artifacts.
2. List the critical claims and entities whose omission could change the decision.
3. Follow explicit references, imports, callers, generated outputs, tests, and manifests.
4. Expand again when a critical claim remains unsupported or evidence conflicts.
5. Use history only to resolve provenance, supersession, or an unexplained decision.

Do not equate more context with better evidence. Record why each additional source is needed and stop loading sources that only duplicate a higher-priority source.

## Artifact lifecycle

Identify the role of an artifact before interpreting drift:

- an immutable release artifact is checked against its release manifest;
- a mutable working copy is expected to diverge after authorized edits;
- a generated or derived artifact is checked against its declared source and generation process.

Ask for user intent when an observed change may be intentional. A hash mismatch proves byte-level difference, not corruption or unauthorized semantic change. Container formats may rewrite multiple internal parts after one user edit; treat those differences as observations until their meaning is established. Do not restore, replace, or overwrite an artifact without authorization.

## Coverage claims

State the denominator and provenance for recall or completeness metrics. If the same investigation both discovers the dependency set and measures recall against it, report `observed recall against the reconstructed set`, not independent or absolute recall. A claim of independently established complete recall requires a frozen external gold set, hidden evaluation notes, or an independent reviewer.

Separate file-count reduction from token, byte, latency, or cost reduction. Do not infer one numeric measure from another without measurement.
