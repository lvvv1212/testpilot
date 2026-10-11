"""AI 回忆故事模块：参数校验（不触发真实生成）。

被测接口：POST /api/story/generate（theme 必填校验）。
空/空白主题会被 Controller 拦截，返回「请选择生成主题」。
"""
from utils.assertions import assert_fail


def test_generate_with_empty_theme(http, base_url, auth_headers):
    """空主题应被拦截。"""
    resp = http.post(
        f"{base_url}/api/story/generate", json={"theme": ""}, headers=auth_headers
    )
    assert_fail(resp, message="请选择生成主题")


def test_generate_with_blank_theme(http, base_url, auth_headers):
    """纯空格主题应被拦截。"""
    resp = http.post(
        f"{base_url}/api/story/generate", json={"theme": "   "}, headers=auth_headers
    )
    assert_fail(resp, message="请选择生成主题")
