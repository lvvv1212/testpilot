# TestPilot

接口自动化测试框架（Python + Pytest + Requests），对 **LifeArchive 后端**（Spring Boot REST API）做接口自动化测试。

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

## 进度

- [x] 阶段 0：脚手架 + venv + 依赖 + Git 初始化
- [x] 阶段 1：被测系统启动，最小闭环跑通（健康检查 + 注册登录 + 错误密码）
- [x] 阶段 2：核心封装（登录态复用 / 数据驱动 / 请求重试 / 统一断言）
- [ ] 阶段 3：用例设计（120+ 条）
- [ ] 阶段 4：Allure 报告 + GitHub Actions
- [ ] 阶段 5：缺陷挖掘与交付
