# Release checklist

- [ ] Version follows `docs/VERSIONING.md`; `1.0` is justified by maturity, not sequence.
- [ ] `pyproject.toml`, `triz_protocol/__init__.py`, `CITATION.cff`, and changelog agree.
- [ ] Unit tests, example validation, benchmark suite, and Markdown link checks pass.
- [ ] A clean environment can install the project and run `triz --help`.
- [ ] Experiment outputs are labeled as real or simulation; no implied empirical claim.
- [ ] No gold set, result leakage, secret, personal data, or closed source is published.
- [ ] User-facing Russian documentation reflects CLI changes.
- [ ] CI and security checks pass before tagging.
