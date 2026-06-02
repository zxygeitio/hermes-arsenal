# Skill/library integrity self-test pattern

Use this reference during Hermes global-control or SRC-framework maintenance when skills or support files are changed.

## What to verify

1. Loaded/modified skills can be `skill_view` loaded.
2. `SKILL.md` references to `references/...` and `scripts/...` exist inside that skill directory.
3. Cross-skill references are either duplicated intentionally or represented by a short forwarding file in the current skill's `references/` directory.
4. Shell helper scripts referenced as executable have `+x` and pass `bash -n`.
5. Python helper scripts pass `py_compile`.
6. Framework smoke tests exercise the actual chain, not just `--help`.

## Minimal reference-check script

```python
import os, re, json
skills = {
    'global-control': '/root/.hermes/skills/ai-development/global-control',
    'src-vuln-hunting': '/root/.hermes/skills/penetration-testing-learning/src-vuln-hunting',
    'education-src-blueprint': '/root/.hermes/skills/penetration-testing-learning/education-src-blueprint',
}
summary = {}
for name, d in skills.items():
    text = open(os.path.join(d, 'SKILL.md'), encoding='utf-8', errors='ignore').read()
    refs = sorted(set(
        re.findall(r'`(references/[^`]+)`', text) +
        re.findall(r'`(scripts/[^`]+)`', text)
    ))
    missing = [r for r in refs if not os.path.exists(os.path.join(d, r.strip()))]
    summary[name] = {'referenced_count': len(refs), 'missing_count': len(missing), 'missing': missing}
print(json.dumps(summary, ensure_ascii=False, indent=2))
```

## Common fixes

- Missing reference that exists in a related umbrella skill: copy concise reference content or add a forwarding reference in the current skill.
- Missing executable bit on a skill script: `chmod +x skill_dir/scripts/name.sh` and verify with `bash -n`.
- `src-http-probe.py` fails on a new workspace path: ensure it creates `workspace.mkdir(parents=True, exist_ok=True)` before writing `probe_results.tsv`.

## Final smoke-test chain

```bash
export LC_ALL=C LANG=C
BASE=/tmp/src-framework-retest-$(date +%s)
INIT_JSON=$(/usr/bin/python3 /root/.hermes/scripts/src-workspace-init.py example.edu.cn --root "$BASE" --scope 'framework retest' --force)
WS=$(/usr/bin/python3 - <<'PY' "$INIT_JSON"
import json,sys
print(json.loads(sys.argv[1])['workspace'])
PY
)
printf '%s\n' 'https://example.com/' 'https://example.com/not-exist-hermes-src-test' > "$WS/urls.txt"
/usr/bin/python3 /root/.hermes/scripts/src-http-probe.py "$WS" "$WS/urls.txt" --timeout 8
/usr/bin/python3 /root/.hermes/scripts/src-quality-gate.py "$WS/probe_results.tsv" --out "$WS/final_gate.md"
/usr/bin/python3 /root/.hermes/scripts/src-js-api-extract.py "$WS" --out "$WS/js_api_findings.json"
head -50 "$WS/final_gate.md"
```

Expected for example.com: `DO_NOT_SUBMIT`, generated headers/bodies, and successful JS/API extraction output.
