# Contributing

1. Separate classical TRIZ terminology from software or AI adaptations.
2. Do not copy matrices, standards, training materials, or examples without a redistribution license.
3. Mark consequential claims as evidence, inference, assumption, or simulation.
4. Prefer falsifiable cases and observable outcomes over persuasive prose.
5. Keep the protocol provider- and model-agnostic.
6. Add a regression test for validator defects.

```bash
python -m unittest discover -s tests -v
python -m triz_protocol validate examples/software/rag-context-contradiction.json
```

A pull request should state the problem, shared benefit, compatibility impact, tests, and provenance/licensing of external material.
