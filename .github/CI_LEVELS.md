# CI levels and budget

The full Python 3.10/3.12/3.13 test/compile/link/example/benchmark matrix remains on PR, main/tag push and manual runs. Feature branch push duplication is removed; use a draft PR or manual run for branch checks. The test job is bounded to ten minutes; existing installation/cache commands are retained.

Manual/tag runs have unique concurrency groups. PR/main updates can supersede stale CI. CodeQL retains main/PR and weekly schedule, permissions, language and twenty-minute limit. Only stale PR security analysis can be cancelled; scheduled/push analyses are independent and retained.

No new release/publication workflow was invented. Public standard runners do not consume private-repository minutes. Local syntax/expression validation passed; hosted compatibility/security verification is pending.
