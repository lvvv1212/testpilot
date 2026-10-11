"""AI 助手模块：参数校验 + 静态接口（不触发真实 RAG 调用）。

被测接口：POST /api/assistant/chat（question 必填校验）、GET /api/assistant/token-usage。
"""
from utils.assertions import assert_ok, assert_fail


def test_chat_with_empty_question(http, base_url, auth_headers):
    """空问题应被拦截。"""
    resp = http.post(
        f"{base_url}/api/assistant/chat", json={"question": ""}, headers=auth_headers
    )
    assert_fail(resp, message="请输入问题")


def test_chat_with_blank_question(http, base_url, auth_headers):
    """纯空格问题应被拦截。"""
    resp = http.post(
        f"{base_url}/api/assistant/chat", json={"question": "   "}, headers=auth_headers
    )
    assert_fail(resp, message="请输入问题")


def test_token_usage(http, base_url, auth_headers):
    """token 用量查询接口应返回 note。"""
    resp = http.get(f"{base_url}/api/assistant/token-usage", headers=auth_headers)
    data = assert_ok(resp)["data"]
    assert "note" in data
