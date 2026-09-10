# TRIZ adaptation for software

This is an analytical mapping, not a claim that software objects are literally classical substances or fields.

| Role | Software interpretation |
|---|---|
| Product | Data, state, output, or user-visible behavior |
| Tool | Function, service, agent, model, or operator |
| Interaction | Call, message, query, event, transformation, or permission |
| Harmful function | Corruption, leakage, latency, irrelevant retrieval, lock-in, unsafe mutation |
| Insufficient function | Missing coverage, weak validation, incomplete retrieval, absent feedback |
| Excessive function | Unnecessary context, duplicate work, over-validation, excessive coupling |
| Resource | Data, metadata, cache, logs, tests, interfaces, compute, time, human review |

Typical candidate contradictions include context coverage versus noise, autonomy versus control, validation confidence versus latency, platform optimization versus portability, and retained history versus current-state pollution. Each relationship must be established for the actual project.
