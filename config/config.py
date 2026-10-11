"""TestPilot 全局配置：被测系统地址与统一约定。

被测系统为 LifeArchive 后端（Spring Boot REST API）。
地址可通过环境变量 LIFEARCHIVE_BASE_URL 覆盖，便于切换本地 / 测试环境。
"""
import os

# 被测系统根地址（默认本机 8080）
BASE_URL = os.getenv("LIFEARCHIVE_BASE_URL", "http://localhost:8080")

# 统一响应码约定（与被测系统 Result 类对齐）
CODE_SUCCESS = 200
CODE_UNAUTHORIZED = 401

# 请求超时（秒），用例需要时传入
TIMEOUT = 10

# 固定测试账号（登录态复用：session 级只登录一次，供鉴权用例共享）
TEST_USERNAME = os.getenv("LIFEARCHIVE_TEST_USER", "testpilot_user")
TEST_PASSWORD = os.getenv("LIFEARCHIVE_TEST_PASS", "Test@123456")
