# Red-Team Flag Mode Runbook

目标：在授权红队攻防/夺旗演练中，用 Hermes 主控进行“低阻塞、可验证、低破坏”的夺旗作业，避免因为工具未开、证据散乱、边界不清或平台限制导致中断。

## 0. 安全边界

开始前必须有：
- 授权范围：IP 段、域名、系统、账号、VPN、时间窗口。
- 规则：允许/禁止的攻击类型、速率限制、是否允许横向、是否允许持久化、flag 提交方式。
- Flag 格式：如 `flag{...}`、`FLAG-...`、文件路径、平台 token。

默认禁止：
- 破坏数据、删改业务数据、写持久化后门。
- 超出授权范围横向移动。
- 批量拖库，除非规则明确要求且只取最小证明。
- 绕过法律/平台限制。

## 1. Hermes 控制模式

Hermes 是主控：负责决策、任务状态、证据、flag ledger、报告。
MCP 是执行器：Burp/HexStrike/扫描器结果必须复核后才进入结论。

按需启动：

```bash
/root/.hermes/scripts/hermes-ensure-tools.sh --gateway --hexstrike
/root/.hermes/scripts/hermes-ensure-tools.sh --burp
```

漏洞情报按需查询：

```bash
/root/.hermes/scripts/hermes-vuln-query.sh --refresh --keyword "产品或CVE" --days 30 --github-limit 10
```

## 2. 工作区

初始化：

```bash
/root/.hermes/scripts/hermes-flag-mode.sh init --case CASE_NAME --target TARGET
```

目录：
- `/root/.hermes/redteam-flag-mode/cases/CASE_NAME/flags.tsv`
- `/root/.hermes/redteam-flag-mode/cases/CASE_NAME/evidence/`
- `/root/.hermes/redteam-flag-mode/cases/CASE_NAME/evidence.tsv`

记录 flag：

```bash
/root/.hermes/scripts/hermes-flag-mode.sh add-flag --case CASE_NAME --target TARGET --flag 'flag{...}' --note 'path/vuln summary'
```

记录证据：

```bash
/root/.hermes/scripts/hermes-flag-mode.sh add-evidence --case CASE_NAME --file /tmp/evidence.txt --note 'HTTP response proving flag access'
```

## 3. 作业流

1. Intake：解析规则、目标、时间窗口、flag 格式。
2. Baseline：检查 VPN split tunnel、Burp/HexStrike/MCP、时间、工作区。
3. Recon：低噪声侦察，先被动/轻量，再主动扫描。
4. Triage：优先能出 flag 的路径：未授权、越权、RCE、文件读取、后台弱口令、CI/CD、对象存储、SSRF、Actuator、Git 泄露。
5. Verify：非破坏性验证，保存请求/响应、截图、命令。
6. Capture：只读取 flag 或最小证明，不扩大数据访问。
7. Submit：输出 flag、路径、命令、证据文件、影响和修复建议。

## 4. Flag 优先级

高优先级路径：
- 明确 flag 文件路径或 hint 暴露。
- 未授权 API 可读 flag/token。
- IDOR 可读目标用户/队伍 flag。
- 文件读取可读 `/flag`、`/root/flag.txt`、应用目录 flag。
- RCE 后 `id` + 读取 flag 文件。
- SSRF 读 metadata/内部 flag 服务。
- 对象存储 bucket/list/read。
- Git/CI/CD 泄露 deploy key 或 flag artifact。

低优先级或慎用：
- 大规模撞库/密码喷洒。
- 需要破坏性写入的利用。
- 持久化、隐藏后门、清痕。

## 5. 输出格式

每个 flag 最终给：
- Target：
- Scope：
- Flag hash / preview：
- Flag 原文：仅在规则允许且用户需要提交时输出；默认 ledger 保存 hash 和 preview。
- Capture path：
- One-line command：
- Evidence file：
- Timestamp：
- Risk / remediation：

## 6. 降级策略

- Burp GUI 开不起来：用 curl/httpx + 保存原始 HTTP 证据；Burp MCP 只作为辅助。
- HexStrike 不可用：用 nmap/nuclei/sqlmap/ffuf 原生命令。
- VPN 影响模型 API：停 VPN，改 split tunnel，验证 API 连通后继续。
- WAF 封禁：停主动探测，转离线 JS/API 分析和已获证据整理。
- GitHub/NVD rate limit：减少 github-limit，使用 searchsploit/nuclei templates/本地缓存。
