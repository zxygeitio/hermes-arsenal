# Seeyou OA (致远OA) 测试模式

## 指纹识别
- URL: oa.xxx.edu.cn/seeyon/
- 登录页: /seeyon/ 或 /seeyon/index.jsp
- CSS引用: /seeyon/common/all-min.css?V=V8_0SP1_YYYYMM_NNNNN
- JS引用: /seeyon/common/all-min.js
- Cookie: JSESSIONID (Path=/seeyon)
- 标题: "xxx协同办公" 或 "xxxOA"

## REST API 端点 (可能未授权)
GET /seeyon/rest/token          → 异常处理页面 (含版本信息)
GET /seeyon/rest/orgMember      → {"code":"1010","message":"被迫下线"}
GET /seeyon/rest/organization   → 同上
GET /seeyon/rest/department     → 同上
GET /seeyon/rest/user           → 同上
GET /seeyon/rest/session        → 同上
POST /seeyon/rest/token         → {"code":500,"message":null}

## Token获取接口
GET /seeyon/rest/token/admin/admin      → 404 (路径不存在)
GET /seeyon/rest/token/admin/123456     → 404
POST /seeyon/rest/token                 → 500错误

## 测试/调试端点
GET /seeyon/test.do     → JS错误页面 ("被迫下线")
GET /seeyon/debug.do    → JS错误页面
GET /seeyon/main.do     → 登录页 (200 OK)

## 信息泄露点
- CSS引用泄露完整版本号: V8_0SP1_201101_29551
- /seeyon/rest/token 返回异常处理页面含版本信息
- /seeyon/common/js/V3X.js 泄露JS框架信息

## 常见漏洞
1. REST API未授权访问 (需验证是否返回真实业务数据)
2. 弱口令 (admin/123456, admin/admin等)
3. 信息泄露 (版本号、内部路径)
4. SQL注入 (登录接口)
5. 文件上传漏洞

## 报告角度
- 致远OA版本泄露 [低危]
- REST API未授权访问 [中危] (需证明可获取敏感数据)
- 弱口令 [高危] (需实际登录成功)
