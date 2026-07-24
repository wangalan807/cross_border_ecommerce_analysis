

import json
from src.services.openrouter_client import get_client


def explain_result_stream(question,tool_result):
    """
    流式生成AI经营顾问建议
    :param question:
    :param tool_result:
    :return:
    """

    tool_result_json = json.dumps(
        tool_result,
        ensure_ascii=False,
        indent=2
    )

    # 保持极其严格的 10 条纯中文自检约束 Prompt
    prompt =f"""
        你是一名跨境电商经营分析顾问。
        用户问题：{question}
        系统分析结果：{tool_result_json}
        角色与任务：
你是一位深耕亚马逊、独立站长达10年的资深跨境电商数据分析专家与商业咨询顾问。请基于下方提供的清洗后多维核心数据字典（含核心财务、用户分层、国家大盘、广告表现指标），为卖家撰写一份结构严谨、逻辑闭环的高级经营洞察与策略报告。

🚨【核心死命令 - 违背任何一条则报告完全作废】：
1. 纯中文输出：整篇报告（包含标题、大纲、正文、甚至图表引用描述）必须采用 100% 纯正、规范的简体中文撰写。
2. 彻底禁用特殊字符：严禁在正文中夹杂任何 Python 代码变量名（如 orders_clean、roi_df、sales_outliers）、下划线（_）、百分号外的奇怪符号或任何未翻译的底层开发标识符。
3. 英文技术词汇强制汉化：凡是触及跨境电商专业术语，必须翻译为标准的中文行业表达。例如：
   - 严禁写 ROI，必须写“投资回报率”或“广告投入产出比”；
   - 严禁写 ACoS / TACOS，必须写“广告销售成本比” / “总广告贡献比”；
   - 严禁写 USA / UK / Germany / Canada / Australia，必须写“美国站”、“英国站”、“德国站”、“加拿大站”、“澳大利亚站”；
   - 严禁写 SKU / FBA，必须写“单品库存单位” / “亚马逊物流配送服务”；
   - 严禁写 High Value / Low Value，必须写“高价值客户群体” / “低价值客户群体”。
4. 数字与货币规范：所有涉及金额的数字，必须保留两位小数，并前置“$”符号或后置“美元”字样。

报告结构规范（请按以下四大模块展开深度分析）：

一、 大盘综合核心业绩审计
   - 提炼总销售额、总订单量、平均客单价的整体财务状况。
   - 针对当前大盘的表现，给出定性的健康度评估（优、良、中、差）。

二、 跨国站点与供应链物流透视
   - 明确指出当前哪一个国家站点是当之无愧的“销售冠军”，其具体的贡献额是多少？
   - 结合物流成本和异常订单，分析哪个站点正在蚕食卖家的利润，并给出供应链优化建议。

三、 用户资产与高价值流失预警
   - 深入分析“高价值客户群体”在总体订单中的占比情况。
   - 探讨如何通过精准营销提高重复购买率，锁定核心利润池。

四、 广告投放ROI（投资回报率）红黑榜与下阶段行动方案
   - 找出表现最好和最差的广告活动/渠道，一针见血地指出钱花在哪里打水漂了，哪里应该加大预算。
   - 给出至少3条下周可直接落地的可执行运营建议。


        """

    client = get_client()
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[{"role":"user","content":prompt}],
        stream=True,
        timeout=30
    )
    # 逐块获取大模型返回的文本段，yield给Streamlit前端
    for chunk in response:
        if hasattr(chunk,'choices') and chunk.choices:
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                yield delta_content