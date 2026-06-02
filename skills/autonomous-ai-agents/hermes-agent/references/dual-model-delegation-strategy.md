# Dual-Model Delegation Strategy

When you have two models with complementary strengths, configure Hermes to use each where it excels:

- **Control plane (model.default)** — the model you chat with. Choose for: large context window, broad reasoning, memory retention, orchestration.
- **Scalpel (delegation.model)** — the model subagents use. Choose for: precision, depth, smaller-but-sharper reasoning on focused tasks.

## Example: mimo-v2.5-pro (1M ctx) + gpt-5.5 (precision)

```yaml
# ~/.hermes/config.yaml

model:
  default: mimo-v2.5-pro
  provider: xiaomi
  base_url: https://token-plan-sgp.xiaomimimo.com/v1
  api_key: ${XIAOMI_API_KEY}

delegation:
  model: gpt-5.5
  provider: custom
  base_url: https://moxinggang.cn/v1
  api_key: <real-key>
  max_iterations: 50
  child_timeout_seconds: 600
  max_concurrent_children: 3
  max_spawn_depth: 1
  orchestrator_enabled: true

custom_providers:
- name: gpt-5.5
  base_url: https://moxinggang.cn/v1
  api_key: <real-key>
  model: gpt-5.5
- name: mimo-v2.5-pro
  base_url: https://token-plan-sgp.xiaomimimo.com/v1
  api_key: ${XIAOMI_API_KEY}
  model: mimo-v2.5-pro
  models:
    mimo-v2.5-pro:
      context_length: 1000000
```

## Key config points

1. `model.*` — your main conversation model. Sets the "brain" of the agent.
2. `delegation.*` — overrides model/provider for `delegate_task` subagents only. When empty, subagents inherit the main model.
3. `custom_providers[].models.<name>.context_length` — sets model-specific context length. **Do NOT use top-level `model.context_length`** as it masks provider-specific values (see custom-provider-context-length.md).
4. Both models must have API keys accessible. For `xiaomi` provider, set `XIAOMI_API_KEY` and optionally `XIAOMI_BASE_URL` in `.env`.

## When to use this pattern

- You have a cheap/fast large-context model and a premium precision model.
- You want to minimize cost on orchestration while keeping depth on focused tasks.
- The control-plane model handles 90% of interaction; delegation fires only for deep dives.

## Pitfalls

- `delegation.base_url` and `delegation.api_key` must be set explicitly when using a custom provider for delegation — they do NOT inherit from `custom_providers`.
- Changes to `model.*` or `delegation.*` require a new session (`/new` or restart CLI) — mid-session switches don't apply.
- If delegation model is empty string, subagents use the main model. This is the default behavior.

## Tuning & Optimization

For production tuning (timeout, iterations, auto_approve, performance benchmarks, task granularity), see **`references/delegation-optimization-guide.md`** in this skill.
