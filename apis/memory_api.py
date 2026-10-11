"""记忆模块接口封装（API Object Model）。

把 /api/memory/* 每个接口封装成方法，用例只调方法、不写裸 URL，
接口路径变更时只需改这一处。创建成功会自动登记 id，供 fixture 统一清理。
"""


class MemoryAPI:
    def __init__(self, session, base_url, headers=None):
        self._session = session
        self._base = base_url
        self._headers = headers or {}
        self.created_ids = []  # 本实例创建的文本记忆 id，供清理

    def create_text(self, title=None, content=None, memory_type=None):
        """POST /api/memory/text 创建文本记忆；成功时登记 id 供清理。"""
        payload = {"title": title, "content": content}
        if memory_type is not None:
            payload["memoryType"] = memory_type
        resp = self._session.post(
            f"{self._base}/api/memory/text", json=payload, headers=self._headers
        )
        body = resp.json()
        if body.get("code") == 200 and body.get("data", {}).get("id"):
            self.created_ids.append(body["data"]["id"])
        return resp

    def list(self, memory_type=None, page=1, size=12):
        """GET /api/memory/list 获取记忆列表（分页）。"""
        params = {"page": page, "size": size}
        if memory_type:
            params["memoryType"] = memory_type
        return self._session.get(
            f"{self._base}/api/memory/list", params=params, headers=self._headers
        )

    def detail(self, memory_id):
        """GET /api/memory/{id} 获取详情。"""
        return self._session.get(
            f"{self._base}/api/memory/{memory_id}", headers=self._headers
        )

    def update(self, memory_id, **fields):
        """PUT /api/memory/{id} 更新字段。"""
        return self._session.put(
            f"{self._base}/api/memory/{memory_id}", json=fields, headers=self._headers
        )

    def delete(self, memory_id):
        """DELETE /api/memory/{id} 删除。"""
        return self._session.delete(
            f"{self._base}/api/memory/{memory_id}", headers=self._headers
        )

    def cleanup(self):
        """删除本实例创建的记忆（已删除/越权错误直接忽略）。"""
        for mid in self.created_ids:
            try:
                self.delete(mid)
            except Exception:
                pass
