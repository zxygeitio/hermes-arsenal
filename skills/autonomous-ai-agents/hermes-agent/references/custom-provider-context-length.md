# Hermes custom provider context length restoration (gpt-5.5 switch)

Session learning: when switching a custom OpenAI-compatible provider from `gpt-5.4` to `gpt-5.5`, do not solve context restoration by setting a broad top-level `model.context_length: 1000000` unless the user explicitly wants a global override.

## Correct pattern

For Hermes Agent custom providers, model-specific context belongs under the provider's `models` map:

```yaml
model:
  default: gpt-5.5
  provider: custom
  base_url: https://example/v1
  api_key: ${KEY}

custom_providers:
- name: gpt5.5
  base_url: https://example/v1
  api_key: ${KEY}
  model: gpt-5.5
  models:
    gpt-5.5:
      context_length: 1050000
```

This lets Hermes resolve the model's own length while avoiding a top-level context override.

## Precedence gotcha

`model.context_length` wins over `custom_providers[].models.<model>.context_length`. If both are set, the top-level value masks the provider-specific value. Remove the top-level line when the user asks for “model来的长度”.

## Safe editing notes

- Prefer targeted patching of `~/.hermes/config.yaml` over `hermes config set` for nested keys that do not already exist.
- Do not write redacted API keys back into config; if a tool output shows `sk-...` redacted, preserve the existing real value or ask the user to restore it.
- After config changes, tell the user to start a new session or `/new` / restart Hermes for startup-read settings to apply.
