"""数据统计模块用例。

被测接口：GET /api/stats/dashboard。
返回结构含 7 个 key：totalMemories / yearlyStats / monthlyStats /
locationStats / emotionStats / typeStats / recentMemories。
"""
from utils.assertions import assert_ok


def test_dashboard_structure(memory, http, base_url, auth_headers):
    """创建记忆后，dashboard 应返回完整统计结构。"""
    assert_ok(memory.create_text(title="统计测试", content="内容"))

    resp = http.get(f"{base_url}/api/stats/dashboard", headers=auth_headers)
    data = assert_ok(resp)["data"]

    expected_keys = {
        "totalMemories", "yearlyStats", "monthlyStats",
        "locationStats", "emotionStats", "typeStats", "recentMemories",
    }
    missing = expected_keys - set(data.keys())
    assert not missing, f"dashboard 缺少字段: {missing}"
    assert data["totalMemories"] >= 1, "totalMemories 应至少为 1"
