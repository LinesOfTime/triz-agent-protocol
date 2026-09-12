# TRIZ Agent Protocol — протокол ТРИЗ для ИИ-агентов

Независимый от конкретной модели протокол доказательного применения подходов ТРИЗ к сложным инженерным, программным, исследовательским и процессным задачам.

```text
facts → functions → causes → contradictions → resources
      → solution concepts → evaluation → verification plan
```

Проект рассчитан на совместную работу людей, Codex, Claude Code, локальных языковых моделей и приложений. Обмен данными выполняется через обычные Markdown- и JSON-файлы. Валидатор использует только стандартную библиотеку Python.

## Зачем нужен проект

Во многих сценариях работа с ТРИЗ сводится к запросу со списком изобретательских принципов. Этот проект требует проверяемого результата: разделения фактов и предположений, функциональной и причинно-конфликтной моделей, формулировки противоречий, учёта доступных ресурсов, сравнения разных механизмов решения, описания рисков и опровергающих проверок.

## Состояние

`0.3.1` — совместимое усиление экспериментальной ветки `0.3`: изолированные пакеты baseline/protocol, контрольные суммы входов, безопасная запись файлов и более строгая проверка парных прогонов. Включённые демонстрационные результаты являются симуляцией и не подтверждают преимущество протокола.

## Быстрый запуск

Требуется Python 3.10 или новее. Сторонние пакеты не нужны.

```bash
python -m triz_protocol init analysis.json --mode lite
python -m triz_protocol analyze analysis.json --problem "Наблюдаемая проблема" --goal "Проверяемая цель"
python -m triz_protocol validate analysis.json
python -m triz_protocol render analysis.json --language ru --output analysis.md
python -m triz_protocol benchmark benchmarks/context-funnel-v1/gold.json benchmarks/context-funnel-v1/result.example.json
python -m triz_protocol prepare-experiment benchmarks/suite-v1/suite.json experiment-001 --protocol-path skills/triz-problem-solving --pair-id pair-001 --model MODEL --model-version VERSION --decoding FIXED
python -m triz_protocol benchmark-suite benchmarks/suite-v1/suite.json benchmarks/suite-v1/results/protocol-demo --output protocol-score.json
python -m triz_protocol compare baseline-score.json protocol-score.json --output comparison.json
python -m unittest discover -s tests -v
```

## Режимы

| Режим | Когда применять | Обязательный анализ |
|---|---|---|
| `lite` | Ограниченная, но нетривиальная задача | Факты, цель, ИКР, противоречие, ресурсы, проверка |
| `analysis` | Повторяющаяся или архитектурная проблема | Lite + функции, причины, альтернативы, оценка |
| `ariz-guided` | Устойчивый конфликт без очевидного решения | Analysis + оперативная зона и время, предельные конфигурации, физическое противоречие |

## Состав репозитория

- `docs/` — методология, терминология, ограничения и интеграция;
- `protocol/` — процедуры для чтения человеком;
- `schemas/` — машиночитаемый контракт;
- `knowledge/` — расширяемые авторские каталоги шаблонов;
- `skills/` — переносимый навык для ИИ-агента;
- `triz_protocol/` — автономный CLI и валидатор;
- `examples/`, `tests/`, `benchmarks/` — примеры, тесты и проверочные наборы.
- `templates/` — готовые формы задачи, контекстной воронки и записи решения.

Подробная установка описана в [docs/installation-ru.md](docs/installation-ru.md), команды — в [docs/commands-ru.md](docs/commands-ru.md), интеграция — в [docs/project-integration-ru.md](docs/project-integration-ru.md), методология оценки — в [docs/evaluation-ru.md](docs/evaluation-ru.md), краткая методология — в [docs/methodology-ru.md](docs/methodology-ru.md), термины — в [docs/terminology-ru.md](docs/terminology-ru.md), план развития — в [docs/ROADMAP.md](docs/ROADMAP.md), правила нумерации — в [docs/VERSIONING.md](docs/VERSIONING.md).

## Ограничения

- Ответ языковой модели является предложением, а не доказательством.
- Протокол требует кратких проверяемых артефактов, а не раскрытия скрытой цепочки рассуждений.
- Репозиторий не содержит скопированных матриц противоречий, текстов стандартных решений, учебных материалов или сторонних разборов.
- Значимые решения требуют профильной экспертизы и независимой проверки.

См. [CONTRIBUTING.md](CONTRIBUTING.md), [ограничения на русском](docs/limitations-ru.md) и [полный англоязычный перечень](docs/limitations.md).

## Лицензия

Код и оригинальные тексты проекта распространяются по лицензии MIT. Названия TRIZ/ТРИЗ и ARIZ/АРИЗ обозначают сложившуюся методологию, связанную с Генрихом Альтшуллером и сообществом ТРИЗ. Внешние материалы в репозиторий не включены.
