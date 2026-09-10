# TRIZ Agent Protocol

A model-agnostic, evidence-aware protocol for applying TRIZ-inspired analysis to difficult engineering, software, research, and process problems.

```text
facts → functions → causes → contradictions → resources
      → solution concepts → evaluation → verification plan
```

The project is usable by humans, Codex, Claude Code, local LLMs, and applications through plain Markdown and JSON. Its validator uses only the Python standard library.

## Why

Many AI workflows reduce TRIZ to a prompt listing inventive principles. This project instead requires inspectable artifacts: evidence labels, functional and cause-conflict models, contradictions, available resources, distinct mechanisms, risks, and falsifiable checks.

## Status

`0.1.0` — usable foundation. Software mappings and Guided ARIZ are original adaptations requiring broader expert review. This is not an official TRIZ implementation or certification.

## Quick start

Requires Python 3.10+ and no third-party packages.

```bash
python -m triz_protocol init analysis.json --mode lite
python -m triz_protocol validate analysis.json
python -m triz_protocol render analysis.json --output analysis.md
python -m unittest discover -s tests -v
```

## Modes

| Mode | Use when | Required analysis |
|---|---|---|
| `lite` | Bounded, non-trivial problem | Facts, goal, IFR, contradiction, resources, verification |
| `analysis` | Recurring or architectural problem | Lite + functions, causes, alternatives, evaluation |
| `ariz-guided` | Persistent conflict without an obvious solution | Analysis + operational zone/time, extreme configurations, physical contradiction |

## Contents

- `docs/`: methodology, terminology, limitations, integration;
- `protocol/`: human-readable procedures;
- `schemas/`: machine-readable contract;
- `knowledge/`: original extensible pattern catalogues;
- `skills/`: portable agent skill;
- `triz_protocol/`: offline CLI and validator;
- `examples/`, `tests/`, `benchmarks/`: evidence of behavior.

## Boundaries

- LLM output is a proposal, not evidence.
- The protocol requests concise reviewable artifacts, not hidden chain of thought.
- It does not include copied contradiction matrices, standard-solution texts, training materials, or third-party case studies.
- High-impact decisions require domain review and independent verification.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/limitations.md](docs/limitations.md).

## License

Code and original project text are MIT licensed. “TRIZ” and “ARIZ” identify an established methodology associated with Genrikh Altshuller and the TRIZ community. External materials are not included.
