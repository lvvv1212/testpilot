"""AI 分析模块：边界与越权用例（不触发真实 LLM 调用）。

被测接口：POST /api/ai/analyze（memoryId 归属校验 + 参数解析）。
这些用例只覆盖「越权」「非法 id」「缺失 id」等前置校验分支，不触发 DeepSeek。
"""
from utils.assertions import assert_ok, assert_fail


def test_analyze_nonexistent_memory(http, base_url, auth_headers):
    """分析不存在的记忆 id 应返回「记忆不存在」。"""
    resp = http.post(
        f"{base_url}/api/ai/analyze", json={"memoryId": 999999999}, headers=auth_headers
    )
    assert_fail(resp, message="记忆不存在")


def test_analyze_other_user_memory(memory, http, base_url, other_auth_headers):
    """越权：用户 B 分析用户 A 的记忆，应被拒绝（对外表现为「记忆不存在」）。"""
    mid = assert_ok(memory.create_text(title="A的记忆", content="内容"))["data"]["id"]

    resp = http.post(
        f"{base_url}/api/ai/analyze", json={"memoryId": mid}, headers=other_auth_headers
    )
    assert_fail(resp, message="记忆不存在")


def test_analyze_invalid_memory_id(http, base_url, auth_headers):
    """非数字 memoryId：应被参数校验拦截，实际抛异常返回 500（缺陷）。"""
    resp = http.post(
        f"{base_url}/api/ai/analyze", json={"memoryId": "abc"}, headers=auth_headers
    )
    assert_fail(resp)


def test_analyze_missing_memory_id(http, base_url, auth_headers):
    """缺失 memoryId：应被参数校验拦截，实际抛空指针返回 500（缺陷）。"""
    resp = http.post(
        f"{base_url}/api/ai/analyze", json={}, headers=auth_headers
    )
    assert_fail(resp)
