"""记忆模块：文本记忆 CRUD 正常链路。

被测接口：/api/memory/text、/api/memory/list、/api/memory/{id}（GET/PUT/DELETE）。
"""
from utils.assertions import assert_ok, assert_fail


def test_create_text_memory(memory):
    """创建文本记忆应返回 id，且字段与入参一致。"""
    resp = memory.create_text(title="我的第一段记忆", content="大学第一次旅行")
    data = assert_ok(resp)["data"]
    assert data["id"], "创建成功但未返回 id"
    assert data["title"] == "我的第一段记忆"
    assert data["content"] == "大学第一次旅行"
    assert data["memoryType"] == "diary"  # 未传 memoryType 时默认 diary
    assert data["fileType"] == "text"


def test_create_and_get_detail(memory):
    """创建后能按 id 取到详情。"""
    mid = assert_ok(memory.create_text(title="详情测试", content="内容A"))["data"]["id"]

    resp = memory.detail(mid)
    data = assert_ok(resp)["data"]
    assert data["id"] == mid
    assert data["title"] == "详情测试"
    assert data["content"] == "内容A"


def test_create_and_list(memory):
    """创建后列表能查到（列表按创建时间倒序，最新在前）。"""
    assert_ok(memory.create_text(title="列表测试", content="列表"))

    resp = memory.list()
    data = assert_ok(resp)["data"]
    assert any(item["title"] == "列表测试" for item in data), "列表未包含刚创建的记录"


def test_list_filter_by_memory_type(memory):
    """按 memoryType 过滤列表只返回对应类型。"""
    assert_ok(memory.create_text(title="日记类", content="x", memory_type="diary"))
    assert_ok(memory.create_text(title="笔记类", content="x", memory_type="note"))

    resp = memory.list(memory_type="note")
    data = assert_ok(resp)["data"]
    assert data, "过滤 note 应有结果"
    assert all(item["memoryType"] == "note" for item in data), "过滤结果混入其他类型"


def test_update_memory(memory):
    """更新 title/content 后详情反映新值。"""
    mid = assert_ok(memory.create_text(title="旧标题", content="旧内容"))["data"]["id"]

    resp = memory.update(mid, title="新标题", content="新内容")
    data = assert_ok(resp)["data"]
    assert data["title"] == "新标题"
    assert data["content"] == "新内容"


def test_delete_memory(memory):
    """删除后再取详情应失败（记忆不存在）。"""
    mid = assert_ok(memory.create_text(title="待删除", content="x"))["data"]["id"]

    assert_ok(memory.delete(mid))

    resp = memory.detail(mid)
    assert_fail(resp, message="记忆不存在")
