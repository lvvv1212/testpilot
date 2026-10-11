"""记忆模块：权限越权用例。

用户 A（主账号）创建的记忆，用户 B（other_auth_headers）无权访问/修改/删除。
越权访问详情返回「记忆不存在」，越权修改/删除返回「无权修改/删除此记忆」。
"""
from utils.assertions import assert_ok, assert_fail


def test_other_user_cannot_get_detail(memory, http, base_url, other_auth_headers):
    """用户 B 访问用户 A 的记忆详情，应被拒绝（对外表现为「记忆不存在」）。"""
    mid = assert_ok(memory.create_text(title="A的私密记忆", content="secret"))["data"]["id"]

    resp = http.get(f"{base_url}/api/memory/{mid}", headers=other_auth_headers)
    assert_fail(resp, message="记忆不存在")


def test_other_user_cannot_update(memory, http, base_url, other_auth_headers):
    """用户 B 修改用户 A 的记忆，应被拒绝。"""
    mid = assert_ok(memory.create_text(title="A的记忆", content="x"))["data"]["id"]

    resp = http.put(
        f"{base_url}/api/memory/{mid}",
        json={"title": "B篡改标题"},
        headers=other_auth_headers,
    )
    assert_fail(resp, message="无权修改此记忆")


def test_other_user_cannot_delete(memory, http, base_url, other_auth_headers):
    """用户 B 删除用户 A 的记忆，应被拒绝。"""
    mid = assert_ok(memory.create_text(title="A的记忆", content="x"))["data"]["id"]

    resp = http.delete(f"{base_url}/api/memory/{mid}", headers=other_auth_headers)
    assert_fail(resp, message="无权删除此记忆")
