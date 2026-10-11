# TestPilot 缺陷报告

> 被测系统：LifeArchive 后端（Spring Boot REST API，`http://localhost:8080`）
> 测试框架：TestPilot（Python + Pytest + Requests + Allure）
> 报告日期：2026-10-11

共发现 **8 个缺陷**：高 1 个、中 5 个、低 2 个。均可在被测系统当前版本稳定复现。

---

## 缺陷清单

| # | 模块 | 标题 | 严重度 | 优先级 |
|---|------|------|--------|--------|
| 1 | 用户 | 空密码可注册成功 | 高 | P1 |
| 2 | 记忆 | 空标题触发数据库错误并泄露 SQL | 中 | P2 |
| 3 | AI 分析 | memoryId 未校验，异常信息泄露 | 中 | P2 |
| 4 | 记忆 | 上传空文件返回成功并创建无效记录 | 中 | P2 |
| 5 | 用户 | 短密码（1 位）可注册成功 | 中 | P2 |
| 6 | 用户 | 非法邮箱格式可注册成功 | 中 | P3 |
| 7 | 记忆 | 更新/删除不存在的 id 提示语不准确 | 低 | P3 |
| 8 | 记忆 | 上传不传文件返回异常提示不友好 | 低 | P3 |

---

## 缺陷详情

### 缺陷 1｜空密码可注册成功（高 / P1）

- **接口**：`POST /api/user/register`
- **复现步骤**：请求体 `{"username":"xxx","password":"","email":"x@x.com"}`
- **实际结果**：返回 `{"code":200,"message":"注册成功","data":{"userId":16,...}}`，空密码用户被创建
- **期望结果**：拒绝注册，返回「密码不能为空」
- **影响**：任何用户可用空密码注册，登录时 `md5("")` 即可匹配，存在账户安全风险
- **建议**：`UserServiceImpl.register` 增加密码非空/长度校验

### 缺陷 2｜空标题触发数据库错误并泄露 SQL（中 / P2）

- **接口**：`POST /api/memory/text`
- **复现步骤**：请求体 `{"title":null,"content":"xxx"}`
- **实际结果**：返回 500，message 为 `Field 'title' doesn't have a default value`，并**泄露完整 SQL 语句与字段名**
- **期望结果**：业务层校验标题必填，返回友好错误「标题不能为空」
- **影响**：参数校验缺失 + 数据库错误信息泄露（SQL 结构暴露）
- **建议**：`MemoryServiceImpl.createTextMemory` 增加标题非空校验

### 缺陷 3｜memoryId 未校验，异常信息泄露（中 / P2）

- **接口**：`POST /api/ai/analyze`
- **复现步骤**：请求体 `{"memoryId":"abc"}`（非数字）或 `{}`（缺失）
- **实际结果**：`Long.valueOf("abc")` 抛 `NumberFormatException` / `NullPointerException`，返回 500 并泄露异常信息
- **期望结果**：参数校验，返回「memoryId 格式错误」
- **影响**：缺少输入校验，异常信息泄露内部实现
- **建议**：`AIController.analyze` 增加 memoryId 存在性与数字格式校验

### 缺陷 4｜上传空文件返回成功并创建无效记录（中 / P2）

- **接口**：`POST /api/memory/upload`
- **复现步骤**：multipart 表单提交 `file` 为空文件
- **实际结果**：返回 `{"code":200,"message":"上传成功"}`，但 `fileUrl=null`、`fileType="other"`，数据库插入一条无文件的记忆
- **期望结果**：拒绝空文件，返回「请选择要上传的文件」
- **影响**：产生 `fileUrl=null` 的垃圾数据，污染列表与统计
- **建议**：`MemoryServiceImpl.saveFile` 对空文件返回 null 时，应直接抛业务异常而非继续入库

### 缺陷 5｜短密码（1 位）可注册成功（中 / P2）

- **接口**：`POST /api/user/register`
- **复现步骤**：请求体 `{"password":"1"}`
- **实际结果**：注册成功
- **期望结果**：拒绝，返回「密码长度至少 N 位」
- **建议**：注册增加密码最小长度校验

### 缺陷 6｜非法邮箱格式可注册成功（中 / P3）

- **接口**：`POST /api/user/register`
- **复现步骤**：请求体 `{"email":"not-an-email"}`
- **实际结果**：注册成功
- **期望结果**：拒绝，返回「邮箱格式错误」
- **建议**：注册增加邮箱格式校验

### 缺陷 7｜更新/删除不存在的 id 提示语不准确（低 / P3）

- **接口**：`PUT /api/memory/{id}`、`DELETE /api/memory/{id}`
- **复现步骤**：对不存在的 id（如 999999999）执行更新/删除
- **实际结果**：返回「无权修改此记忆」/「无权删除此记忆」
- **期望结果**：返回「记忆不存在」（当前实现把"不存在"与"越权"归为同一分支）
- **影响**：提示语误导用户，不利于排查

### 缺陷 8｜上传不传文件返回异常提示不友好（低 / P3）

- **接口**：`POST /api/memory/upload`
- **复现步骤**：非 multipart 请求，不携带 file
- **实际结果**：返回 500，message 为 `Current request is not a multipart request`
- **期望结果**：返回友好提示「请使用文件上传表单」
- **影响**：异常信息直接透出，缺少友好包装

---

## 说明

- 上述缺陷均为对被测系统当前版本的真实观测结果，复现步骤可直接在本地执行验证。
- 缺陷用例已固化在 `cases/` 目录（如 `test_memory_boundary.py::test_create_memory_without_title`），
  其余通过接口直接探测确认，详见本报告各条「复现步骤」。
- 被测系统修复后，对应用例应同步更新断言。
