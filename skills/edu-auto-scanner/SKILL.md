---
name: edu-auto-scanner
description: "教育SRC全自动化扫描工具集 — 批量探测+指纹→漏洞映射+JS安全分析+workspace持久化"
category: penetration-testing-learning
tags: [src, edu, automation, scanner, fingerprint, recon]
created_by: agent
---

# 教育SRC自动化扫描工具集

## 触发条件
- 用户要求对教育/高校目标进行自动化扫描
- 需要批量子域探测、指纹识别、漏洞扫描
- 需要断点续扫、状态持久化

## 工具清单

所有脚本位于 `/root/.hermes/scripts/`:

| 脚本 | 功能 | 用法 |
|------|------|------|
| `edu-batch-probe.py` | 批量子域探测+指纹 | `python3 edu-batch-probe.py subs.txt --dns -f` |
| `auto-vuln-scan.py` | 指纹→漏洞自动映射 | `python3 auto-vuln-scan.py https://target --enum` |
| `js-secrets-scanner.py` | JS安全分析 | `python3 js-secrets-scanner.py bundle.js` |
| `src-workspace.py` | 扫描状态持久化 | `python3 src-workspace.py init domain` |
| `edu-full-scan.py` | 全自动扫描主控 | `python3 edu-full-scan.py domain` |

## 使用流程

### 一键全自动
```bash
/usr/bin/python3 /root/.hermes/scripts/edu-full-scan.py target.edu.cn
```

### 分步执行(推荐，可人工干预)
```bash
# 1. 初始化workspace
/usr/bin/python3 /root/.hermes/scripts/src-workspace.py init target.edu.cn

# 2. 批量探测
/usr/bin/python3 /root/.hermes/scripts/edu-batch-probe.py subs.txt --dns -f -o alive.txt

# 3. 提取URL
awk '{print $3}' alive.txt | grep '://' > urls.txt

# 4. 自动漏洞扫描
/usr/bin/python3 /root/.hermes/scripts/auto-vuln-scan.py urls.txt --enum --workspace target.edu.cn

# 5. JS安全分析(对SPA目标)
/usr/bin/python3 /root/.hermes/scripts/js-secrets-scanner.py https://target/assets/index.js --url

# 6. 查看结果
/usr/bin/python3 /root/.hermes/scripts/src-workspace.py status target.edu.cn
```

### 断点续扫
```bash
/usr/bin/python3 /root/.hermes/scripts/src-workspace.py resume target.edu.cn
```

## 内置指纹库

auto-vuln-scan.py 内置以下产品指纹:
- 致远OA (Seeyon) — REST API、thirdpartyController、downloadServlet
- CAS统一认证 — 用户枚举、API信息泄露、微信AppID泄露
- Spring Boot Actuator — health/env/heapdump/mappings
- Druid监控 — 登录页、数据源泄露、SQL监控
- Swagger UI — API文档泄露
- 泛微OA (Weaver) — 代码数据、微信配置
- 金智教育CAS — 密钥泄露、验证码检查
- Sangfor WebVPN — 登录用户枚举、密钥登录
- Visual SiteBuilder (VSB) — 配置文件
- Apache Shiro — rememberMe Cookie
- Tomcat/Nginx — 管理页面、状态页

## 性能指标(实测)

| 场景 | 耗时 | 说明 |
|------|------|------|
| 20子域 DNS+HTTP探活+指纹 | 4.5s | DNS并行+HTTP并行 |
| 10目标 自动漏洞扫描 | ~60s | 8-10个端点/目标 |
| 单目标 JS分析(2MB) | ~3s | 25+规则匹配 |
| 用户枚举(16用户名) | ~30s | 串行避免封禁 |

## 踩坑记录 (Pitfalls)

### Python路径
- **必须用 `/usr/bin/python3`**，不要用 `python3`（可能是shim，10秒超时）
- 所有脚本shebang已设为 `#!/usr/bin/python3`
- `edu-full-scan.py` 内部subprocess也用 `/usr/bin/python3`

### DNS过滤: timeout命令会干扰subprocess输出捕获
- ❌ `subprocess.run(['timeout', '2', 'dig', '+short', sub, 'A'], capture_output=True)` → stdout为空
- ✅ `subprocess.run(['dig', '+short', sub, 'A'], capture_output=True, timeout=3)` → 正常
- **原因**: `timeout`命令的管道行为在capture_output模式下不可靠
- **正确做法**: 去掉`timeout` wrapper，只用subprocess的`timeout`参数

### 用户枚举: 单indicator不够
- CAS系统对不同用户名返回的错误信息格式不固定
- ✅ 用`exists_indicators`列表: `['登录失败', '微信扫码', '校园网外', '密码错误', '验证码']`
- ✅ 用`notexists_indicators`列表: `['账号不存在', '用户不存在', '用户名不存在']`
- 两端都不匹配时标记为UNKNOWN，不误判

### 指纹库扩展
- 新增指纹写到 `auto-vuln-scan.py` 的 `FINGERPRINT_DB` 字典
- 格式: `{name, match: {headers: [], body: [], cookies: []}, paths: [(path, method, desc, severity, is_vuln_func)]}`
- `is_vuln_func` 接收body字符串，返回bool
- 待扩展: 用友/金蝶/蓝凌/通达/浪潮/正方/强智/青果/金智/树维

### Workspace集成
- `auto-vuln-scan.py --workspace <domain>` 自动保存漏洞到workspace
- workspace目录: `/tmp/vuln_reports/<domain>/`
- `src-workspace.py list` 查看所有工作区

## 关联技能
- 指纹库和漏洞模式: 见 `src-vuln-hunting` skill
- 教育供应商识别: 见 `src-vuln-hunting` 的 `references/edu-vendor-fingerprinting.md`
- CAS漏洞模式: 见 `src-vuln-hunting` 的 `references/cas-vuln-testing-patterns.md`
- CERNET网络策略: 见 `pentest-recon-driven` 的 `references/cuit-edu-testing-patterns.md`

## 漏洞结果需人工复核，自动扫描可能有误报
