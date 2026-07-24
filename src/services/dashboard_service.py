

import pandas as pd

def build_dashboard_data(report_data):

    country_sales = pd.DataFrame(
        report_data["country_metrics"]["country_sales"]
    )

    if country_sales.empty:
        return {
            "success": False,
            "message": "暂无国家销售数据"
        }

    # 🔹 如果列名不是 'sales'（根据你的分析模型上游决定），先尝试做一次重命名
    if 'revenue' in country_sales.columns:
        country_sales = country_sales.rename(columns={"revenue": "sales"})



    high_value_ratio = report_data["user_metrics"]["high_value_ratio"]
    user_health = (
        "good" if high_value_ratio > 0.25
        else "warning"
    )


    if "sales" not in country_sales.columns:
        return {
            "success":False,
            "message": "country_sales缺少sales列"
        }
    country_sales_sorted = (country_sales.sort_values(
        by="sales",
        ascending=False
    )
    )

    daily_sales = pd.DataFrame(
        report_data["time_metrics"]["daily_sales"]
    )

    if daily_sales.empty:
        daily_sales = pd.DataFrame(
            columns=["order_date","sales"]
        )

    return {
        "success": True,

        "user_health": user_health,
        "country_sales": country_sales,
        "country_sales_sorted": country_sales_sorted,
        "top3_country": country_sales_sorted.head(3),
        "bottom3_country": country_sales_sorted.tail(3),
        "best_sales_country": report_data["country_metrics"]["best_sales_country"],
        "best_country_sales": report_data["country_metrics"]["best_country_sales"],
        "worst_sales_country": report_data["country_metrics"]["worst_sales_country"],
        "worst_country_sales":report_data["country_metrics"]["worst_country_sales"],
        "daily_sales": daily_sales,
        "best_day": report_data["time_metrics"]["best_day"],
        "worst_day": report_data["time_metrics"]["worst_day"],
    }
