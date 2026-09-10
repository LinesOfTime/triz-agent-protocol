# Methodology

The protocol produces a compact, inspectable model before proposing changes. Analysis depth is proportional to uncertainty, contradiction strength, and consequence of error.

## Workflow

1. Establish known facts and provenance.
2. State the observable goal and invariants.
3. Formulate the Ideal Final Result (IFR) without prescribing implementation.
4. Identify useful, harmful, insufficient, and excessive interactions.
5. Trace harmful effects toward controllable causes.
6. State the technical contradiction as an improvement and deterioration.
7. When supported, state the physical contradiction.
8. Locate conflict in space, time, condition, and system level.
9. Inventory existing resources before adding components.
10. Generate mechanically distinct concepts.
11. Evaluate each dimension transparently.
12. Define tests capable of disproving the preferred concept.

## Evidence discipline

- `evidence`: directly supported by an observable source;
- `inference`: derived from stated evidence;
- `assumption`: plausible but unestablished;
- `simulation`: intentionally invented for exploration.

Repeated model output never upgrades an assumption to evidence.

## IFR form

```text
The system provides [useful result] using [available resources],
without [harm or forbidden change], while [invariant remains true].
```

## Evaluation

Score expected benefit, movement toward IFR, resource use, verifiability, complexity, risk, reversibility, and compatibility from 0 to 5 with a justification. Never treat the combined number as authorization.
