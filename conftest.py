"""全局 fixture：会话级 HTTP 客户端、请求重试、登录态复用、记忆模块客户端。

能力清单：
1. http          —— 会话级 requests.Session，挂载重试适配器（网络抖动自动重试）
2. base_url      —— 被测系统根地址
3. auth_headers  —— 登录主测试账号（session 级只登录一次）
4. other_auth_headers —— 登录第二个测试账号（越权用例用）
5. memory        —— 记忆模块客户端（function 级，自动清理本用例创建的记忆）
"""
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from apis.memory_api import MemoryAPI
from config.config import (
    BASE_URL,
    TEST_USERNAME,
    TEST_PASSWORD,
    OTHER_USERNAME,
    OTHER_PASSWORD,
)
from utils.assertions import assert_ok


def _build_session():
    """构造带重试能力的 Session：只重试网络层错误，业务错误不重试。"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    # 被测系统在本机，必须直连，不能被系统 HTTP 代理拦截（否则连 localhost 会返回 502）
    session.trust_env = False

    # 重试策略：连接失败 / 读超时 最多重试 3 次，指数退避；不重试业务 5xx
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=0.5,
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "PATCH"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _login_headers(http, base_url, username, password):
    """登录指定账号（不存在则先注册），返回带 token 的请求头。"""
    resp = http.post(f"{base_url}/api/user/login", json={
        "username": username,
        "password": password,
    })
    if resp.json()["code"] != 200:
        http.post(f"{base_url}/api/user/register", json={
            "username": username,
            "password": password,
            "email": f"{username}@example.com",
        })
        resp = http.post(f"{base_url}/api/user/login", json={
            "username": username,
            "password": password,
        })

    body = assert_ok(resp)
    token = body["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def base_url():
    """被测系统根地址。"""
    return BASE_URL


@pytest.fixture(scope="session")
def http():
    """会话级 requests.Session，统一挂载公共请求头与重试策略。"""
    session = _build_session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def auth_headers(http, base_url):
    """主测试账号的鉴权头（session 级只登录一次）。"""
    return _login_headers(http, base_url, TEST_USERNAME, TEST_PASSWORD)


@pytest.fixture(scope="session")
def other_auth_headers(http, base_url):
    """第二个测试账号的鉴权头（越权用例用）。"""
    return _login_headers(http, base_url, OTHER_USERNAME, OTHER_PASSWORD)


@pytest.fixture
def memory(http, base_url, auth_headers):
    """记忆模块客户端（function 级，用例结束自动清理其创建的记忆）。"""
    client = MemoryAPI(http, base_url, auth_headers)
    yield client
    client.cleanup()
