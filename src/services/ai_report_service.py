
from src.services.openrouter_client import get_client
import hashlib
import json

#  AI经营分析报告
def get_data_hash(data):
    return hashlib.md5(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()


def build_report_prompt(report_data):
    core = report_data.get('core_metrics', {})
    user = report_data.get('user_metrics', {})
    sales = core.get('total_sales', 0)
    orders = core.get('total_orders', 0)
    aov = core.get('avg_order_value', 0)
    country = core.get('best_sales_country', 'N/A')
    users = user.get('total_users', 0)
    high_value_pct = f"{user.get('high_value_ratio', 0):.2%}"

    prompt = f"""
    你是一名顶级咨询公司大中华区的跨境电商板块的资深合伙人，请基于以下跨境电商数据，输出一份“高管级经营分析报告”。
    【基础经营数据快照】
    - 周期内总销售额（Total Revenue）: {sales}
    - 业务总订单量（Total Orders）: {orders}
    - 平均客单价（AOV）: {aov}
    - 核心主力突破市场（Top Country）: {country}
    - 活跃客户基数（Total Customer Base）: {users}
    - 核心高价值贡献客户占比（High-Value Ratio）: {high_value_pct}

    【经营数据快照（仅作为您分析的底层论据，绝对禁止在报告中直接机械照抄这些干巴巴的数字）：】
    - 总营收表现: {sales}
    - 基础交易量: {orders}
    - 平均客单价水平: {aov}
    - 核心主力市场: {country}
    - 活跃客户基数: {users}
    - 高价值客户贡献占比: {high_value_pct}

    输出要求：

    "输出要求：请全程使用专业、商务的简体中文撰写报告。如涉及国家名称、数据指标，
    请尽量转换为中文术语（例如将 'US' 转化为 '美国'），但无需刻意抹去必要的阿拉伯数字。"
    最终输出必须为100%纯简体中文。

    请开始撰写高管级全景战略报告：

    【一】执行摘要 
    请用宏观的视角概述本周期的整体跨境经营态势。

    【二】核心发现
    针对以该突破性国家为代表的主力市场进行深度战略复盘。

    【三】问题诊断
    对当前业务暴露出的一系列隐患进行严肃的外科手术式诊断。

    【四】增长机会
    站在战略顾问视角，推演后续的破局红利。

    【五】行动建议
    请提供一套具备强落地指导意义的阶段性企业治理规划。

    【六】风险提示
    针对当前极端集中的数据趋势与国际地缘局势，为高管层拉响警报。
    """

    return prompt

def generate_ai_report(report_data):
    client = get_client()

    prompt = build_report_prompt(report_data)


    response = client.chat.completions.create(
        model="qwen/qwen-2.5-7b-instruct:free",
        messages=[
            {"role": "system",
            "content": "你是顶级咨询公司的资深合伙人，"
                       "专注跨境电商战略分析。请严格使用简体中文输出，"
                       "禁止出现任何英文或其他非中文字符。"
             },
            {
                "role": "user",
                "content": prompt
            }
        ],
        timeout=60
    )
    return response.choices[0].message.content or "AI未返回内容"



#  彻底重构后的 AI 报告流式输出函数
def generate_ai_report_stream(report_data):
    client = get_client()
    prompt = build_report_prompt(report_data)

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是顶级咨询公司的资深合伙人，专注跨境电商战略分析。请全程使用专业、商务的简体中文撰写报告。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True,
        timeout=120  # 💡 建议从 60 延长到 120，防止大模型思考时间过长导致超时断开
    )

    for chunk in response:
        # 🔥 核心修正：必须先确保 choices 存在且不为空列表，否则会报 IndexError
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0].delta

            # 兼容普通内容输出和深度思考模型的思考内容
            content = getattr(delta, "content", None)

            if content:
                yield content
