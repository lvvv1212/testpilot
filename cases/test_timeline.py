"""时间轴模块用例。

被测接口：GET /api/timeline/list、GET /api/timeline/year/{year}。
时间轴按记忆 eventTime 升序、按年份分组返回。
"""
import datetime

from utils.assertions import assert_ok


def test_timeline_contains_created_memory(memory, http, base_url, auth_headers):
    """创建文本记忆后，时间轴列表应包含该记录。"""
    mid = assert_ok(memory.create_text(title="时间轴测试", content="内容"))["data"]["id"]

    resp = http.get(f"{base_url}/api/timeline/list", headers=auth_headers)
    data = assert_ok(resp)["data"]

    all_ids = [event["memoryId"] for node in data for event in node.get("events", [])]
    assert mid in all_ids, "时间轴未包含刚创建的记录"


def test_timeline_by_current_year(memory, http, base_url, auth_headers):
    """按当前年份过滤时间轴，应包含今年创建的记录。"""
    mid = assert_ok(memory.create_text(title="今年记忆", content="内容"))["data"]["id"]
    current_year = datetime.date.today().year

    resp = http.get(f"{base_url}/api/timeline/year/{current_year}", headers=auth_headers)
    data = assert_ok(resp)["data"]
    ids = [event["memoryId"] for node in data for event in node.get("events", [])]
    assert mid in ids


def test_timeline_by_old_year_is_empty(memory, http, base_url, auth_headers):
    """查询久远年份（1999）应返回空列表。"""
    resp = http.get(f"{base_url}/api/timeline/year/1999", headers=auth_headers)
    data = assert_ok(resp)["data"]
    assert data == [], f"1999 年不应有记忆，实际: {data}"
