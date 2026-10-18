# QueryPilot

Ask business questions in plain language. A self-correcting agent writes, validates, runs and repairs SQL, then returns a table, a chart and a plain-language explanation.

> *"Which 5 customers spent the most in 2013, by country?"* → table + chart + explanation. Follow-ups like *"and for 2012?"* reuse conversation context.

## Pipeline

```
Question → Schema retrieval → SQL generation → Validate + run (sandbox) → Self-repair loop → Table, chart, explanation
```

## Agent tools

| Tool | Purpose |
|---|---|
| `list_tables()` / `describe_table(name)` | Schema exploration (introspection, embedding retrieval for large DBs) |
| `sample_rows(table, n)` | Real values (formats, codes) shown to the model |
| `validate_sql(query)` | Rejects anything that is not a single SELECT (sqlglot) |
| `run_query(query, limit, timeout)` | Read-only connection, timeout, row cap |
| `plot(result, chart_type)` | Chart of the result |
| `explain_result(question, result)` | Explanation constrained to returned rows |

## Roadmap

- [ ] **Phase 1** – chat loop, sessions, tool-calling loop, schema tools, safe execution
- [ ] **Phase 2** – self-repair (error + empty-result feedback), retry budget, attempt logging
- [ ] **Phase 3** – schema linking, few-shot retrieval by similarity
- [ ] **Phase 4** – Spider / BIRD benchmark (execution accuracy) + ablations
- [ ] **Phase 5** – UI: chat, SQL viewer, charts, history

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env          # add your API key
bash scripts/get_chinook.sh   # downloads demo DB into data/
pytest
```

## Evaluation plan

Execution accuracy on fixed samples (~300 questions) of Spider and BIRD. Ablations: no repair vs repair, full vs retrieved schema, zero-shot vs retrieved few-shot. Also: avg attempts per question, and share of harmful queries blocked.

## Layout

```
src/querypilot/
  agent/    chat loop, sessions, self-repair
  tools/    schema, validator, executor, plot, explain
  llm/      provider client + prompts
  schema/   schema linking / retrieval
  eval/     benchmark harness
  ui/       web UI
```

## Team

See [CONTRIBUTING.md](CONTRIBUTING.md) for the ownership split.
