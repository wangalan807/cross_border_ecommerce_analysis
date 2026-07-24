
from dotenv import load_dotenv
from openai import OpenAI
import os
import httpx


#  1. 加载本地环境变量
load_dotenv()

#  2. 统一环境变量名称，确保与你的终端和全局配置 100% 一致
openrouter_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_key:
    raise ValueError(
        "未找到OPENROUTER_API_KEY"
    )

#  3. 初始化符合 OpenRouter 规范的 OpenAI 客户端
def get_client():
    return  OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            http_client=httpx.Client(
               # proxy="http://127.0.0.1:29290",
                trust_env=False
            )
    )
"""
def get_client():
    # 因为开启了 TUN 模式，不需要再手动指定 127.0.0.1 的本地端口
    # 只需要配置一个高超时的 httpx 客户端即可，它会自动走虚拟网卡
    return OpenAI(
        api_key=openrouter_key,
        base_url="https://openrouter.ai/api/v1",
        http_client=httpx.Client(
            timeout=120.0  # 延长超时到 120 秒，防止洛杉矶节点高峰期握手失败
        )
    )
"""
