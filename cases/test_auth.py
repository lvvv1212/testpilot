"""用户模块用例：注册 → 登录 → 鉴权（阶段 1 最小闭环）。

被测接口：
- POST /api/user/register  注册（重复用户名/邮箱会返回业务码 500）
- POST /api/user/login     登录，成功返回 data.token

注意：被测系统对业务异常仍返回 HTTP 200，仅 body.code != 200，
因此断言需同时校验 HTTP 状态码（协议层）与业务码（业务层）。
"""
import time

from config.config import CODE_SUCCESS


def _unique_username(prefix="tester"):
    """生成唯一用户名，避免重复注册冲突。"""
    return f"{prefix}_{int(time.time() * 1000)}"


def test_register_and_login(http, base_url):
    """正常链路：注册新用户 → 用该账号登录 → 拿到 token。"""
    username = _unique_username()
    password = "Test@123456"

    # 1. 注册
    resp = http.post(f"{base_url}/api/user/register", json={
        "username": username,
        "password": password,
        "email": f"{username}@example.com",
    })
    assert resp.status_code == 200, f"注册 HTTP 状态异常: {resp.status_code}"
    assert resp.json()["code"] == CODE_SUCCESS, f"注册失败: {resp.text}"

    # 2. 登录
    resp = http.post(f"{base_url}/api/user/login", json={
        "username": username,
        "password": password,
    })
    assert resp.status_code == 200, f"登录 HTTP 状态异常: {resp.status_code}"
    body = resp.json()
    assert body["code"] == CODE_SUCCESS, f"登录失败: {resp.text}"
    assert body["data"]["token"], "登录成功但未返回 token"


def test_login_with_wrong_password(http, base_url):
    """负向用例：错误密码登录应返回业务码非 200，且提示「用户名或密码错误」。"""
    username = _unique_username(prefix="wrongpwd")

    http.post(f"{base_url}/api/user/register", json={
        "username": username,
        "password": "Right@123",
        "email": f"{username}@example.com",
    })

    resp = http.post(f"{base_url}/api/user/login", json={
        "username": username,
        "password": "Wrong@123",
    })
    assert resp.status_code == 200  # 业务异常仍返回 HTTP 200（全局异常处理器）
    body = resp.json()
    assert body["code"] != CODE_SUCCESS, f"错误密码不应登录成功: {resp.text}"
    assert "用户名或密码错误" in body["message"]
