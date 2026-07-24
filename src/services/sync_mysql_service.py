import pandas as pd

from src.database import get_connection

from src.loader import (
    load_orders,
    load_ads
)

from src.analyzer import (
    convert_order_date,
    add_sales_column,
    add_time_features,
    add_user_value_segment,
    detect_outliers,
    add_conversion_rate,
    get_country_sales,
    calculate_roi,
    get_daily_sales
)



def sync_mysql_service():
    """
    全流程自动化业务调度服务：连接->提取->清洗->评估->输出分析报告
    :return:
    """
    try:
        conn = get_connection()
        raw_orders = load_orders(conn)
        ad_df = load_ads(conn)
        print(f"成功从数据库中读取{len(raw_orders)}条订单流水和{len(ad_df)}条广告流水！")

        # 2. 调用你写的 analyzer 模块进行高性能清洗
        orders_clean = convert_order_date(raw_orders)
        orders_clean = add_sales_column(orders_clean)
        orders_clean = add_time_features(orders_clean)
        orders_clean = add_user_value_segment(orders_clean)

        #  显式检查
        if "sales" not in orders_clean.columns:
            orders_clean["sales"] = orders_clean["unit_price"] * orders_clean["quantity"]

        # 顺便揪出异常值，为简历增加硬核亮点
        sales_outliers = detect_outliers(orders_clean, 'sales')
        ad_clean = add_conversion_rate(ad_df)

        # 跨表高级核心指标运算（按国家聚合广告成本后再算 ROI）
        country_sales = get_country_sales(orders_clean)
        roi_df = calculate_roi(country_sales, ad_clean)
        country_metrics_df = roi_df
        daily_sales = get_daily_sales(orders_clean)

        # 3. 完美对齐你原本的 report_data 商业指标结构
        total_sales = orders_clean["sales"].sum()
        total_orders = len(orders_clean)
        avg_order_value = total_sales / total_orders if total_orders > 0 else 0

        # 找出最好的国家和销售额，最差的国家和销售额
        best_sales_country = country_sales.loc[country_sales["sales"].idxmax()]["country"] if not country_sales.empty else "N/A"
        best_country_sales = country_sales["sales"].max() if not country_sales.empty else 0
        worst_sales_country = country_sales.loc[country_sales["sales"].idxmin()]["country"] if not country_sales.empty else "N/A"
        worst_country_sales = country_sales["sales"].min() if not country_sales.empty else 0

        # 高价值用户占比（按独立用户数计算）
        total_users = orders_clean["user_id"].nunique()
        high_value_users = orders_clean.loc[
            orders_clean["user_value_segment"] == "High Value", "user_id"
        ].nunique()
        high_value_ratio = high_value_users / total_users if total_users > 0 else 0

        # 时间序列分析
        best_day = daily_sales.loc[daily_sales["sales"].idxmax()]
        worst_day = daily_sales.loc[daily_sales["sales"].idxmin()]




        report_data = {
            "success": True,
            "core_metrics": {
                "total_sales": round(total_sales, 2),
                "total_orders": int(total_orders),
                "avg_order_value": round(avg_order_value, 2),
                "best_sales_country": best_sales_country
            },
            "user_metrics": {
                "total_users": int(total_users),
                "high_value_ratio": round(high_value_ratio, 4)
            },
            "country_metrics": {
                "best_sales_country": best_sales_country,
                "best_country_sales": round(best_country_sales,2),
                "worst_sales_country": worst_sales_country,
                "worst_country_sales": round(worst_country_sales,2),
                "country_sales": country_sales.to_dict("records") if not country_sales.empty else [],
                 },
            "time_metrics": {
                "daily_sales": daily_sales.to_dict("records") if not daily_sales.empty else [],
                "best_day": {
                    "order_date":str(best_day["order_date"]),
                    "sales":float(best_day["sales"])
                } if not daily_sales.empty else {"order_date":"N/A","sales":0},
                "worst_day":{
                    "order_date":str(worst_day["order_date"]),
                    "sales":float(worst_day["sales"])
                } if not daily_sales.empty else {"order_date":"N/A","sales":0}
            },
            "sales_outliers": sales_outliers.to_dict("records") if isinstance(sales_outliers,pd.DataFrame) else [],
            "roi_metrics": roi_df.to_dict("records") if isinstance(roi_df,pd.DataFrame) else [],

            "country_metrics_df":country_metrics_df,
            "roi_df":roi_df,
            "daily_sales_df":daily_sales,
            "orders_df":orders_clean
        }
        print("🎉 整个后端调度数据流清洗成功！各项宏观指标已成功解耦并生成报告。")
        return report_data


    except Exception as e:
        print(f"调度系统运行发生错误：{e}")
        return {
            "success": False,
            "message": str(e)
        }