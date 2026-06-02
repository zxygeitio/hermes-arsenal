# SRC Authorized Research Control Policy

Created: 2026-05-24
Owner: local Hermes controller
Purpose: maximize high-value SRC research efficiency while keeping evidence reproducible, low-impact, and within authorized scope.

## Standing authorization interpretation

The user authorized Hermes to optimize local SRC/red-team research tooling and to autonomously conduct authorized vulnerability research. The user may manually provide accounts, but expects Hermes to automatically gather all other obtainable context: assets, historical URLs, JS/API routes, fingerprints, public intelligence, local tool status, evidence files, and report material.

Treat the authorization as permission to:

- optimize local Hermes/SRC tooling, workspaces, scripts, skills, MCP/Burp/HexStrike/Gateway usage, and evidence storage;
- run reconnaissance, vulnerability discovery, and red-team style attack-chain validation on targets that are in a stated SRC / owned / lab / exercise scope;
- automatically start local support services such as Burp, HexStrike, Gateway, browsers, and workspace scripts when needed;
- automatically collect passive/public intelligence, certificate transparency data, historical URLs, JS bundles, API paths, screenshots, and response evidence;
- use authenticated test accounts, cookies, tokens, and captured traffic when the user provides them or when accounts are self-created according to the target program rules;
- prove impact with the minimum safe operation necessary and produce only verified, reproducible vulnerability reports.

This authorization still does NOT create permission to attack arbitrary third parties outside a stated scope or to perform unnecessary destructive actions. Maintain legal/scope boundaries and prefer minimal-impact proof.

Do not repeatedly ask for permission to perform ordinary research steps. Ask only when the missing item cannot be obtained by tools and materially changes legality or safety, such as: target scope is unknown, credentials/account state is required, a destructive action would be needed, or a third-party service/account would be affected.

It does NOT authorize:

- destructive actions outside explicit exercise rules, malware, extortion, credential theft, data exfiltration beyond minimal proof, or bypassing legal target scope;
- high-volume brute force, password spraying, SMS/email bombing, DoS, mass data scraping, or financially impactful operations;
- using third-party accounts/tokens without authorization;
- modifying or deleting real target data except harmless test records created by us and cleaned up when possible.

## Default low-impact verification limits

Unless the target program explicitly allows more:

- IDOR/object enumeration: <= 20 IDs per endpoint, stop immediately after proving boundary issue.
- Sensitive data capture: minimize and redact; save only enough fields to prove impact.
- File upload: harmless HTML/text/image only; no executable webshells or malware; include cleanup if delete endpoint exists.
- SMS/email: <= 2 manual proof sends per recipient/flow; no loops.
- Auth testing: no credential stuffing; only provided/self-owned accounts.
- Rate: conservative throttling; prefer single-shot controls over scanners on business APIs.

## High-value priority matrix

P0/P1 only unless user explicitly asks otherwise:

1. RCE / command injection / deserialization with safe proof only.
2. SQL injection with minimal proof and no bulk dump.
3. Authentication bypass / token forgery / unsigned session.
4. IDOR / horizontal or vertical privilege boundary breach using A/B accounts.
5. Unauthenticated sensitive business data API.
6. File upload that creates accessible, renderable, user-impacting content or leads to stored XSS/phishing proof within rules.
7. API key/AppSecret exposure only if it can call real data or quota/resource endpoints.
8. Mass assignment / quota / role / ownerId / status tampering.

Discard or mark non-submit by default:

- SPA fallback, WAF block pages, failed 403/404/500 only, static public config, version leakage alone, clickjacking alone, weak CORS with no credentialed sensitive read, DMARC alone, fixed low-impact values, theoretical-only issues.

## Required per-target inputs for full power

Create `/tmp/vuln_reports/<target>/target_profile.md` with:

- Program/scope URL and allowed domains/IPs.
- Explicit exclusions and prohibited tests.
- Account matrix: anonymous, user A, user B, special roles if available.
- Cookies/tokens storage paths, never pasted into final report unredacted.
- Core business flows and valuable object IDs.
- Allowed verification limits if different from defaults.
- Prior submissions/ignored findings/dedupe notes.

## Workspace standard

For each target:

```bash
/usr/bin/python3 /root/.hermes/scripts/src-workspace-init.py <target> --scope '<authorized scope summary>'
```

Then use:

- `assets.tsv` for domains/IPs.
- `endpoints.tsv` for URLs/API paths.
- `probe_results.tsv` for normalized probes.
- `negative.md` for dead ends and false positives.
- `candidate_reports/` for unverified drafts.
- `final_reports/` only after verified proof.
- `headers/` and `bodies/` for reproducible evidence.

Run quality gates before report output:

```bash
/usr/bin/python3 /root/.hermes/scripts/src-quality-gate.py "$WS/probe_results.tsv" --target-profile /tmp/vuln_reports/<target>/target_profile.md --out "$WS/final_gate.md"
/usr/bin/python3 /root/.hermes/scripts/src-report-format-gate.py "$WS/final_reports/report.txt"
```

## Agent execution mode

- Use Hermes main controller for decisions, value judgment, dedupe, and final reports.
- Use MCP/HexStrike/Burp as execution engines only; verify their results manually.
- Use background processes or cron only for passive/low-impact discovery and change detection.
- Use `todo` for active multi-step work; one `in_progress` item.
- Do not ask the user to operate tools manually when the local tool can do it.
- If required authorization/account context is missing and cannot be retrieved, proceed with anonymous recon but label high-risk/high-value findings as needing account-state verification.
