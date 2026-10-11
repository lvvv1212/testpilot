"""统一断言：收敛「HTTP 状态码 + 业务码」的双层判断逻辑。

被测系统约定：业务异常（如密码错误、用户名重复）仍返回 HTTP 200，
仅 body.code != 200。因此断言必须同时看协议层（status_code）与业务层（code）。
"""
from config.config import CODE_SUCCESS


def assert_ok(resp):
    """断言协议层与业务层都成功，返回响应体 dict。

    适用：所有预期成功的接口调用。
    """
    assert resp.status_code == 200, f"HTTP 状态码异常: {resp.status_code}，响应: {resp.text}"
    body = resp.json()
    assert body["code"] == CODE_SUCCESS, f"业务码异常: {body.get('code')}，响应: {resp.text}"
    return body


def assert_fail(resp, message=None):
    """断言业务失败：HTTP 200 但 body.code != 200；可选校验 message 子串。

    适用：预期失败的负向用例（错误密码、越权、参数非法等）。
    """
    assert resp.status_code == 200, f"HTTP 状态码异常: {resp.status_code}，响应: {resp.text}"
    body = resp.json()
    assert body["code"] != CODE_SUCCESS, f"预期失败但业务码为成功，响应: {resp.text}"
    if message is not None:
        assert message in body.get("message", ""), f"错误提示不匹配，响应: {resp.text}"
    return body
