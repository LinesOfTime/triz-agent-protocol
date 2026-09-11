# TRIZ Agent Protocol Benchmark Suite v1

Набор проверяет структурные свойства ответа, а не абстрактную «изобретательность». Он заморожен до оцениваемых прогонов, но ещё не прошёл независимую экспертную рецензию.

## Слепой прогон

1. Исполнителю передаются только `task.md` и `evidence.json` каждого кейса. Для контекстной воронки передаются `task.md` и каталог `repository/` из соседнего `context-funnel-v1`.
2. `gold.json` и демонстрационные результаты не включаются в контекст модели.
3. Сначала выполняется baseline без протокола, затем — отдельный прогон с протоколом. Порядок следует чередовать между моделями, чтобы снизить влияние порядка.
4. Результаты сохраняются под идентификаторами кейсов в отдельных каталогах.
5. Каждый каталог оценивается `benchmark-suite`; полученные сводки сравниваются командой `compare`.

```bash
triz benchmark-suite benchmarks/suite-v1/suite.json results/baseline --output baseline-score.json
triz benchmark-suite benchmarks/suite-v1/suite.json results/protocol --output protocol-score.json
triz compare baseline-score.json protocol-score.json --output comparison.json
```

Демонстрационный каталог `results/protocol-demo/` проверяет только работу оценщика. Он не является результатом реального запуска модели и не доказывает преимущество протокола.
