# Model-agnostic integration

Use `protocol/` directly with any model, install the included skill, or integrate through structured JSON:

1. collect a problem statement;
2. generate JSON conforming to `schemas/analysis.schema.json`;
3. validate locally;
4. return errors for correction;
5. render the accepted artifact for human review.

Keep protocol, validation, storage, and domain decisions independent of model providers. A suitable boundary is:

```python
class LLMGateway:
    def generate_structured(self, messages, schema): ...
```

The CLI is offline. Network behavior depends on the chosen agent and provider.
