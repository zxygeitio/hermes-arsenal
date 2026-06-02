---
name: hermes-agent-self-evolution
description: |
  Evolutionary self-improvement for Hermes Agent using DSPy + GEPA (Genetic-Pareto Prompt Evolution).
  Automatically evolves and optimizes skills, tool descriptions, system prompts, and code through
  reflective evolutionary search. No GPU training required — operates via API calls.
category: ai-development
---

# Hermes Agent Self-Evolution

Evolutionary self-improvement using DSPy + GEPA (Genetic-Pareto Prompt Architecture).

## Source
https://github.com/NousResearch/hermes-agent-self-evolution

## Quick Start

```bash
cd /tmp/hermes-agent-self-evolution
pip install -e ".[dev]"

# Point at your hermes-agent repo
export HERMES_AGENT_REPO=~/.hermes/hermes-agent

# Evolve a skill (synthetic eval data)
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source synthetic

# Or use real session history
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source sessiondb
```

## System Optimization Audit

When the user asks to inspect or optimize the whole Hermes Agent system, use the reusable audit pattern in `references/system-optimization-audit.md`. It covers baseline discovery, skill dedupe, MCP health separation, cron hygiene, repo update safety, and the important rule to run repo tests with the Hermes venv Python rather than system Python.


                                      │
                                      ▼
                                 GEPA Optimizer ◄── Execution traces
                                      │                    ▲
                                      ▼                    │
                                 Candidate variants ──► Evaluate
                                      │
                                 Constraint gates (tests, size limits, benchmarks)
                                      │
                                      ▼
                                 Best variant ──► PR against hermes-agent
```

## Key Files

- `evolution/skills/evolve_skill.py` — Main skill evolution script
- `generate_report.py` — Evolution report generator
- `datasets/` — Eval datasets
- `tests/` — Test suites
