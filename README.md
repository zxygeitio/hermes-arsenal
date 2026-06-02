# Hermes Arsenal

A comprehensive collection of security skills, automation scripts, and agent configurations for Hermes Agent — focused on penetration testing, SRC vulnerability hunting, CTF, and red team operations.

## Overview

This repository contains:
- **Penetration Testing Skills** — 30+ specialized skills covering web pentest, SRC hunting, exploit chains, lateral movement, and more
- **Automation Scripts** — Python/bash scripts for vulnerability scanning, CORS testing, IDOR detection, API reconnaissance
- **Red Team Framework** — Red team flag mode, evidence collection, report generation
- **MCP Integrations** — Burp Suite, HexStrike, and other tool integrations
- **Education SRC Toolkit** — Specialized patterns for Chinese education institution vulnerability research

## Quick Start

```bash
# 1. Clone to ~/.hermes
git clone https://github.com/zxygeitio/hermes-arsenal.git ~/.hermes

# 2. Configure environment
cp ~/.hermes/.env.example ~/.hermes/.env
cp ~/.hermes/config.yaml.example ~/.hermes/config.yaml
# Edit .env and config.yaml with your API keys

# 3. Initialize Hermes
hermes setup
```

## Directory Structure

```
~/.hermes/
├── skills/                          # Agent skills (core value)
│   ├── penetration-testing-learning/  # Pentest skills collection
│   │   ├── src-vuln-hunting/          # SRC vulnerability hunting
│   │   ├── exploit-chain/             # End-to-end exploit chains
│   │   ├── ctf-playbook/              # CTF competition playbook
│   │   ├── pentest-recon-driven/      # Recon-driven pentest
│   │   └── ...                        # 25+ more skills
│   ├── ai-development/              # AI agent development skills
│   ├── productivity/                # Feishu, email, docs
│   └── ...                          # MLOps, DevOps, etc.
├── scripts/                         # Automation scripts
│   ├── src-*.py                     # SRC testing tools
│   ├── edu-*.py                     # Education SRC automation
│   ├── pentest_*.py                 # Pentest framework
│   └── hermes-*.sh                  # System management
├── redteam-flag-mode/               # Red team exercise framework
├── src-control/                     # SRC policy & optimization
├── .env.example                     # Environment template
├── config.yaml.example             # Config template
└── SOUL.md                          # Agent persona
```

## Key Skills

### Penetration Testing
- **src-vuln-hunting** — SRC vulnerability hunting workflow
- **exploit-chain** — End-to-end attack chains (SQLi, SSRF, file upload, etc.)
- **pentest-recon-driven** — Recon-driven penetration testing
- **web-pentest-fast** — Quick web pentest decision tree
- **pentest-lateral** — Lateral movement & internal network

### SRC Specialization
- **education-src-blueprint** — Chinese education institution SRC
- **src-vuln-hunting** — General SRC hunting methodology
- **vuln-intel** — Vulnerability intelligence aggregation

### Red Team
- **redteam-flag-mode** — Authorized red team exercises
- **post-exploit-pwncat** — Post-exploitation & stable control
- **cicd-pipeline-poisoning** — CI/CD infrastructure abuse

### Automation
- **edu-auto-scanner** — Education SRC batch scanning
- **auto-recon-lowhanging** — Automated recon & low-hanging fruit

## Scripts

| Script | Description |
|--------|-------------|
| `src-idor-check.py` | IDOR vulnerability detection |
| `src-cors-batch-test.py` | CORS misconfiguration testing |
| `src-sqli-hunter.py` | SQL injection hunting |
| `src-rce-scanner.py` | RCE vulnerability scanning |
| `src-js-api-extract.py` | JavaScript API extraction |
| `edu-batch-probe.py` | Education domain batch probing |
| `pentest_engine.py` | Pentest automation engine |

## Security Notice

**This repository is for authorized security testing only.**

- Always obtain proper authorization before testing
- Follow responsible disclosure practices
- Respect scope limitations and rules of engagement
- Do not use for unauthorized access or malicious purposes

## Configuration

### Environment Variables

Required:
- `OPENROUTER_API_KEY` — For LLM access (via OpenRouter)

Optional integrations:
- `FEISHU_APP_ID` / `FEISHU_APP_SECRET` — Feishu bot
- `TELEGRAM_BOT_TOKEN` — Telegram bot
- `GITHUB_TOKEN` — GitHub API access
- `TAVILY_API_KEY` — Web search API

### MCP Servers

Configure MCP servers in `config.yaml`:
```yaml
mcp:
  servers:
    hexstrike:
      command: /path/to/hexstrike
    burpsuite:
      command: /path/to/burp-mcp
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your skills/scripts
4. Ensure no credentials are hardcoded
5. Submit a pull request

## License

MIT License — See LICENSE file for details

## Disclaimer

This tool is provided for legitimate security testing purposes only. Users are responsible for ensuring they have proper authorization before using these tools against any system. The authors are not responsible for any misuse or damage caused by this tool.

---

**Built with [Hermes Agent](https://hermes-agent.nousresearch.com) — The autonomous AI agent framework**
