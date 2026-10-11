"""冒烟用例：被测系统健康检查接口。

这是 TestPilot 的第一条用例，用于验证「框架 → 请求 → 断言」整条链路可用。
被测系统未启动时，本用例会因连接被拒绝而失败（属预期，见 README 启动说明）。
"""


def test_health_check(http, base_url):
    """健康检查应返回 200，且 data 标记应用为 running。"""
    resp = http.get(f"{base_url}/api/health")
    assert resp.status_code == 200, f"HTTP 状态码异常: {resp.status_code}"

    body = resp.json()
    assert body["code"] == 200, f"业务码异常: {body.get('code')}"
    assert body["data"]["status"] == "running"
    assert body["data"]["app"] == "LifeArchive"
