# SRC High-Value Optimization Checklist

## What is now locally ready

- Gateway/Burp/HexStrike status should be checked with `/root/.hermes/scripts/hermes-ensure-tools.sh --status`.
- Evidence/report roots:
  - `/tmp/vuln_reports`
  - `/tmp/src-workspaces`
  - `/root/.hermes/src-control`
- Core workflow scripts:
  - `/root/.hermes/scripts/src-workspace-init.py`
  - `/root/.hermes/scripts/src-http-probe.py`
  - `/root/.hermes/scripts/src-js-api-extract.py`
  - `/root/.hermes/scripts/src-quality-gate.py`
  - `/root/.hermes/scripts/src-report-format-gate.py`

## Per-target quick start

```bash
export LC_ALL=C LANG=C
TARGET='example.com'
INIT_JSON=$(/usr/bin/python3 /root/.hermes/scripts/src-workspace-init.py "$TARGET" --scope 'authorized low-impact SRC verification')
WS=$(/usr/bin/python3 - <<'PY' "$INIT_JSON"
import json,sys
print(json.loads(sys.argv[1])['workspace'])
PY
)
echo "$WS"
```

## Inputs that most improve high-risk findings

1. Two low-privilege accounts A/B for horizontal authorization checks.
2. One special-role account if program allows supplier/student/merchant/admin-low role testing.
3. Captured Burp traffic for login, query, create, update, upload, export, download, password reset.
4. A few real but self-owned object IDs: orderId, fileId, userId, orgId, applicationId, invoiceId, ticketId.
5. Program scope and exact prohibited actions.

## Default high-yield tests after traffic capture

- Remove Authorization/Cookie and replay.
- Replace A object IDs in B session.
- Replace orgId/tenantId/deptId/schoolId/companyId.
- Check server-controlled fields in JSON/body: user_id, ownerId, role, status, quota, price, amount, isAdmin, auditStatus.
- Try list/export endpoints with pageSize inflation within safe limits.
- Test file download URLs for predictable IDs or missing signature.
- Test upload endpoint auth, content-type, path, access URL, delete cleanup.
- Test API key creation/update for mass assignment and immediate usable proof, then delete.
- Test JWT/session signing only on owned accounts.

## External API keys that would improve asset discovery

Add to `/root/.hermes/.env` when available; do not paste secrets into reports:

- FOFA_KEY / FOFA_EMAIL
- HUNTER_API_KEY
- QUAKE_TOKEN
- SHODAN_API_KEY
- CENSYS_API_ID / CENSYS_API_SECRET
- ZOOMEYE_API_KEY
- SECURITYTRAILS_API_KEY
- CHAOS_KEY
- GITHUB_TOKEN already appears configured

## Current non-blocking gaps observed on 2026-05-24

- `tlsx` install failed due transient GitHub/network reset; not critical because `openssl`/`httpx` can cover TLS basics.
- If `httpx` is the Python package instead of ProjectDiscovery binary on a command path, prefer explicit ProjectDiscovery install later.
- Nuclei templates exist under `/root/nuclei-templates`; keep updating before CVE/template-driven runs.

## Report gate reminder

Only produce final reports after:

- command actually executed locally;
- response body/header evidence saved;
- no-token/invalid-token or A/B account control performed;
- duplicate/root cause checked against `/tmp/vuln_reports`;
- screenshot locations identified;
- single-line curl commands verified.
