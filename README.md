# TestPilot

接口自动化测试框架（Python + Pytest + Requests + Allure），对 **LifeArchive 后端**（Spring Boot REST API）做接口自动化测试。

[![API Tests](https://github.com/lvvv1212/testpilot/actions/workflows/test.yml/badge.svg)](https://github.com/lvvv1212/testpilot/actions/workflows/test.yml)

> 项目已完成：35 条用例覆盖 14 个接口，GitHub Actions 全量回归全绿。

## 被测系统

- LifeArchive 后端：`http://localhost:8080`
- 统一响应格式：`{"code": 200, "message": "...", "data": {...}}`
- 鉴权：`Authorization: Bearer <token>`；免鉴权路径：`/api/health`、`/api/user/login`、`/api/user/register`

## 目录结构

```
TestPilot/
├── config/    # 环境配置（base_url、响应码约定）
├── apis/      # 接口封装层（每个接口一个方法）
├── cases/     # 测试用例层
├── data/      # 数据驱动（yaml/json 测试数据）
├── utils/     # 公共能力（登录态、断言、请求封装）
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## 快速开始

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

## 测试报告（Allure）

生成并查看 Allure HTML 报告：

```bash
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
# 打开 allure-report\index.html 即可查看
```

Windows 下可直接双击 `run_allure.bat` 一键生成（需先安装 [Allure CLI](https://github.com/allure-framework/allure2/releases) 并加入 PATH）。

## 进度

- [x] 阶段 0：脚手架 + venv + 依赖 + Git 初始化
- [x] 阶段 1：被测系统启动，最小闭环跑通（健康检查 + 注册登录 + 错误密码）
- [x] 阶段 2：核心封装（登录态复用 / 数据驱动 / 请求重试 / 统一断言）
- [x] 阶段 3：用例设计 — 覆盖 user / memory / timeline / stats / ai / story / assistant 七模块，共 35 条
- [x] 阶段 4：Allure 报告 + GitHub Actions — 本地报告已生成，CI 全绿（run#3 success）
- [x] 阶段 5：缺陷挖掘与交付 — 缺陷报告见 [docs/DEFECTS.md](docs/DEFECTS.md)

## 测试中发现的缺陷

完整缺陷报告见 [docs/DEFECTS.md](docs/DEFECTS.md)，共 **8 个缺陷**（高 1 / 中 5 / 低 2）。

| # | 模块 | 缺陷 | 严重度 |
|---|------|------|--------|
| 1 | 用户 | 空密码可注册成功 | 高 |
| 2 | 记忆 | 空标题触发数据库错误并泄露 SQL | 中 |
| 3 | AI分析 | memoryId 未校验，异常信息泄露 | 中 |
| 4 | 记忆 | 上传空文件返回成功并创建无效记录 | 中 |
| 5 | 用户 | 短密码（1 位）可注册成功 | 中 |
| 6 | 用户 | 非法邮箱格式可注册成功 | 中 |
| 7 | 记忆 | 更新/删除不存在的 id 提示语不准确 | 低 |
| 8 | 记忆 | 上传不传文件返回异常提示不友好 | 低 |
