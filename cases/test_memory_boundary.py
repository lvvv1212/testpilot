"""记忆模块：参数边界与异常用例。

记录被测系统在边界输入下的真实行为，部分属于潜在缺陷（见用例注释）。
"""
from utils.assertions import assert_ok, assert_fail


def test_get_nonexistent_memory(memory):
    """查询不存在的 id 应返回「记忆不存在」。"""
    resp = memory.detail(999999999)
    assert_fail(resp, message="记忆不存在")


def test_update_nonexistent_memory(memory):
    """更新不存在的 id 应失败。

    注意：后端实现里 selectById 为空与「越权」走同一分支，返回「无权修改此记忆」，
    语义上应提示「记忆不存在」——这是被测系统的一个提示语缺陷，此处仅断言其失败。
    """
    resp = memory.update(999999999, title="x")
    assert_fail(resp)


def test_delete_nonexistent_memory(memory):
    """删除不存在的 id 应失败。"""
    resp = memory.delete(999999999)
    assert_fail(resp)


def test_create_memory_without_title(memory):
    """空标题记忆：应被业务层拒绝并给出友好提示（缺陷）。

    实际行为：后端未校验标题，title=null 穿透到数据库，MySQL 报
    「Field 'title' doesn't have a default value」，后端返回 500，
    且 message 泄露了 SQL 语句与字段名（信息泄露）。
    期望行为：业务层校验标题必填，返回友好错误（如「标题不能为空」）。
    """
    resp = memory.create_text(title=None, content="无标题内容")
    assert_fail(resp)


def test_create_memory_without_content(memory):
    """空内容：后端当前不校验，创建会成功。"""
    resp = memory.create_text(title="只有标题", content=None)
    assert assert_ok(resp)["data"]["id"]


def test_create_memory_default_type(memory):
    """不传 memoryType 时默认 diary。"""
    resp = memory.create_text(title="默认类型", content="x")
    assert assert_ok(resp)["data"]["memoryType"] == "diary"
