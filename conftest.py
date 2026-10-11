"""全局 fixture：会话级 HTTP 客户端与基础地址。

后续阶段会把「登录态复用」也挂到这里的 session 级 fixture 上，
做到登录一次、所有用例共享 token。
"""
import pytest
import requests

from config.config import BASE_URL


@pytest.fixture(scope="session")
def base_url():
    """被测系统根地址。"""
    return BASE_URL


@pytest.fixture(scope="session")
def http():
    """会话级 requests.Session，统一挂载公共请求头。"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    # 被测系统在本机，必须直连，不能被系统 HTTP 代理拦截（否则连 localhost 会返回 502）
    session.trust_env = False
    yield session
    session.close()
