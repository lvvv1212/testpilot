"""用户模块用例：注册、登录、鉴权。

覆盖：
- 注册 → 登录 → 拿 token（正链路）
- 登录负向（数据驱动：密码错误 / 空密码 / 用户不存在）
- 带 token 访问鉴权接口（登录态复用演示）
"""
import time

import pytest

from config.config import TEST_USERNAME
from utils.assertions import assert_ok, assert_fail
from utils.data_loader import load_json

# 登录负向用例数据（数据驱动：逻辑与数据分离）
_LOGIN_FAIL_CASES = load_json("login_cases.json")


def _unique_username(prefix="tester"):
    """生成唯一用户名，避免重复注册冲突。"""
    return f"{prefix}_{int(time.time() * 1000)}"


def test_register_and_login(http, base_url):
    """正常链路：注册新用户 → 用该账号登录 → 拿到 token。"""
    username = _unique_username()
    password = "Test@123456"

    resp = http.post(f"{base_url}/api/user/register", json={
        "username": username,
        "password": password,
        "email": f"{username}@example.com",
    })
    assert_ok(resp)

    resp = http.post(f"{base_url}/api/user/login", json={
        "username": username,
        "password": password,
    })
    body = assert_ok(resp)
    assert body["data"]["token"], "登录成功但未返回 token"


@pytest.mark.parametrize("case", _LOGIN_FAIL_CASES, ids=lambda c: c["name"])
def test_login_negative(http, base_url, case):
    """负向用例：异常凭据登录应业务失败，且提示「用户名或密码错误」。"""
    username = case.get("username", TEST_USERNAME)
    resp = http.post(f"{base_url}/api/user/login", json={
        "username": username,
        "password": case["password"],
    })
    assert_fail(resp, message=case["message"])


def test_get_user_info_with_token(http, base_url, auth_headers):
    """鉴权接口：带 token 访问 /api/user/info，应返回当前登录用户。"""
    resp = http.get(f"{base_url}/api/user/info", headers=auth_headers)
    body = assert_ok(resp)
    assert body["data"]["username"] == TEST_USERNAME


def test_get_user_info_without_token(http, base_url):
    """鉴权接口：不带 token 访问应返回 401（拦截器直接写 401 响应）。"""
    resp = http.get(f"{base_url}/api/user/info")
    assert resp.status_code == 401, f"未携带 token 应返回 401，实际: {resp.status_code}"
    assert resp.json()["code"] == 401
