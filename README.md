# TestPilot

接口自动化测试框架（Python + Pytest + Requests + Allure），对 **LifeArchive 后端**（Spring Boot REST API）做接口自动化测试。

[![API Tests](https://github.com/lvvv1212/testpilot/actions/workflows/test.yml/badge.svg)](https://github.com/lvvv1212/testpilot/actions/workflows/test.yml)

> 项目处于搭建阶段。当前进度见下方「进度」。

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
- [ ] 阶段 3：用例设计（120+ 条）— 已覆盖 user/memory/timeline/stats/ai/story/assistant 七模块（35 条），待补图片上传与更多边界组合
- [ ] 阶段 4：Allure 报告 + GitHub Actions — 本地报告已生成，CI 工作流已写好（push 到 GitHub 后生效）
- [ ] 阶段 5：缺陷挖掘与交付

## 测试中发现的缺陷

| # | 模块 | 缺陷描述 | 严重度 | 状态 |
|---|------|----------|--------|------|
| 1 | 记忆 | 创建记忆时标题为空，后端未校验，穿透到 MySQL 报「Field 'title' doesn't have a default value」，返回 500 且 message 泄露 SQL 与字段信息 | 中 | 待修复 |
| 2 | AI分析 | analyze 接口未校验 memoryId，传非数字/缺失时抛 NumberFormatException/NullPointerException 返回 500，泄露异常信息 | 中 | 待修复 |
| 3 | 记忆 | 更新/删除不存在的 id 返回「无权修改/删除此记忆」而非「记忆不存在」，提示语不准确 | 低 | 待修复 |
