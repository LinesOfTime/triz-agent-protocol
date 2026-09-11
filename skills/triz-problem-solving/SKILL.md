---
name: triz-problem-solving
description: Structure difficult engineering, software, research, or process problems using evidence-aware TRIZ analysis. Use when requirements conflict, fixes repeat, architecture choices create trade-offs, or the user requests TRIZ or ARIZ. Skip routine implementation with an established solution.
---

# TRIZ Problem Solving

Produce concise, reviewable problem models and solution concepts. Do not claim hidden reasoning or expert certification. LLM assertions are not evidence.

Write user-facing analysis in the user's language. Preserve machine identifiers and source references exactly.

## Select the lightest sufficient mode

- **Lite:** bounded non-trivial problem. Read `references/triz-lite.md`.
- **Analysis:** recurring, architectural, or causally unclear problem. Also read `references/advanced-analysis.md`.
- **Guided ARIZ:** persistent strong contradiction after ordinary analysis. Read both references.

For repository context selection, artifact drift, or coverage claims, also read `references/context-evidence.md`.

When designing or interpreting an evaluation of this protocol, read `references/evaluation.md`. Do not load it for ordinary problem solving.

## Shared requirements

1. Establish system boundary, facts, goal, and invariants.
2. Label claims as evidence, inference, assumption, or simulation.
3. Formulate the IFR without embedding a preferred solution.
4. Identify the contradiction before selecting mechanisms.
5. Inventory existing resources before proposing dependencies or services.
6. Generate at least two mechanically distinct concepts.
7. State risks and tests capable of rejecting each concept.
8. Recommend only a reversible next step when evidence is incomplete.

When the repository is available, produce JSON matching `schemas/analysis.schema.json`. Otherwise use Markdown with the same logical fields.

Stop and request evidence or a decision when boundaries are unknown, an essential causal link is unsupported, invariants conflict, the next action is irreversible, or domain authorization is required.

For terminology and adaptation boundaries, read `references/boundaries.md` when the distinction affects the answer.
