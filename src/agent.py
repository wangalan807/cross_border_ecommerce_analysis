
from src.tools import (
get_top_roi_country,
get_bottom_sales_country,
get_top_sales_country,
get_lowest_roi_country,
get_best_sales_day,
get_worst_sales_day,
get_high_value_user_stats,
get_ad_candidates
)
from rapidfuzz import fuzz


#  为route_question增加模糊匹配提问
INTENT_LIBRARY = {
    "top_sales_country":[
        "哪个国家销售额最高",
        "销售额最高国家",
        "卖得最好的国家",
        "销量冠军国家",
        "哪个市场卖得最好"
    ],

    "bottom_sales_country":[
        "哪个国家销售额最低",
        "卖得最差国家",
        "销量最低国家"
    ],

    "top_roi_country":[
        "哪个国家ROI最高",
        "ROI最好国家",
        "投资回报率最高国家"
    ],

    "lowest_roi_country":[
        "哪个国家ROI最低",
        "ROI最差国家"
    ],

    "best_sales_day":[
        "哪一天销售最好",
        "销售最高的一天",
        "销量最高日期"
    ],

    "worst_sales_day":[
        "哪一天销售最差",
        "销售最低的一天",
        "销售最低日期"
    ],

    "high_value_user":[
        "高价值用户占比",
        "VIP用户占比",
        "高价值客户比例"
    ],

    "ad_candidates":[
        "哪些国家值得增加广告预算",
        "广告应该投哪里",
        "哪个市场值得加预算"
    ]
}
def route_question(question,country_df=None,roi_df=None,daily_df=None,orders_df=None):
    """
        简单的Question Router：
        根据问题关键词调用对应的 Tool。

        参数：
            question (str): 用户输入的问题
            country_df, roi_df, daily_df, orders_df: 对应数据表格

        返回：
            dict: 统一结构化结果，来自对应Tool
        """

    question = question.strip()
    intent,score = detect_intent(question)


    #  设置阈值
    if score < 70:
        return {
            "success": False,
            "tool":None,
            "intent":intent,
            "score":score,
            "message":"暂时无法识别该问题",
            "data":None
        }

    #  销售分析
    if intent == "top_sales_country":
        result =  get_top_sales_country(country_df)
    elif intent == "bottom_sales_country":
        result = get_bottom_sales_country(country_df)
    elif intent == "best_sales_day":
        result = get_best_sales_day(daily_df)
    elif intent == "worst_sales_day":
        result = get_worst_sales_day(daily_df)

    #  ROI分析
    elif intent == "top_roi_country":
        result = get_top_roi_country(roi_df)
    elif intent == "lowest_roi_country":
        result = get_lowest_roi_country(roi_df)

    #  用户分析
    elif intent == "high_value_user":
        result = get_high_value_user_stats(orders_df)

    #  广告预算
    elif intent == "ad_candidates":
        result = get_ad_candidates(country_df)

    else:
        return {
            "success": False,
            "tool":None,
            "message":"问题无法匹配到现有的Tool中",
            "data":None
        }

    if result:
        result["intent"] = intent
        result["score"] = score
    return result

#  写一个意图识别函数
def detect_intent(question):
    best_intent = None
    best_score = 0

    for intent,examples in INTENT_LIBRARY.items():
        for example in examples:
            score = fuzz.partial_ratio(
                question.lower(),
                example.lower()
            )

            if  score > best_score:
                best_score = score
                best_intent = intent

    return best_intent,best_score