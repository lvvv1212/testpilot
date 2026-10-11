"""数据驱动：从 data/ 目录加载 JSON 测试数据。

用例通过 pytest.mark.parametrize 消费这些数据，实现「用例逻辑」与「测试数据」分离。
"""
import json
import os

# data/ 目录绝对路径（相对本文件定位，避免依赖运行时的 cwd）
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def load_json(filename):
    """读取 data/ 下的 JSON 文件并返回解析结果。"""
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
