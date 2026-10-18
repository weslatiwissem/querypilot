# Contributing

## Ownership
| Member | Owns |
|---|---|
| A | From-scratch loop, sessions/follow-ups, safe execution layer (`agent/`, `tools/validator.py`, `tools/executor.py`) |
| B | SQL generation prompts, schema linking, few-shot retrieval, self-repair (`llm/`, `schema/`) |
| C | Benchmark harness, charts, explanations, UI (`eval/`, `tools/plot.py`, `ui/`) |

## Workflow
- Branch from `main`: `feat/<area>-<short-name>`; open a PR, one review minimum.
- CI (ruff + pytest) must pass.
- Benchmark runs cost credits: use the fixed 300-question sample, once per major change; commit result JSONs under `docs/results/`.
