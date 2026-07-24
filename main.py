
import os
from src.loader import load_orders,load_ads
from src.database import get_connection
from src.analyzer import (
    convert_order_date,
    add_sales_column,
    add_time_features,
    add_conversion_rate,
    get_country_sales,
    calculate_roi,
    get_daily_sales,
    add_user_value_segment,
    get_kpi_metrics,
    check_data_ready,
    detect_outliers,
    top_n_by_column
)





def main() -> None:


    #  1. 获取数据库连接
    conn = get_connection()
    #  2. 从 MySQL 加载原始数据
    orders_df = load_orders(conn)
    ad_df = load_ads(conn)



    #  3. 数据清晰和指标计算
    orders_clean = convert_order_date(orders_df)
    orders_clean = add_sales_column(orders_clean)
    orders_clean = add_time_features(orders_clean)
    orders_clean = add_user_value_segment(orders_clean)
    sales_outliers = detect_outliers(orders_clean,'sales')
    print("销售额异常值：")
    print(sales_outliers)


    ad_clean = add_conversion_rate(ad_df)

    country_sales = get_country_sales(orders_clean)
    roi_df = calculate_roi(country_sales,ad_clean)
    conversion_df = ad_clean
    daily_sales = get_daily_sales(orders_clean)
    kpi_metrics = get_kpi_metrics(
        orders_clean,
        country_sales,
        roi_df,
        conversion_df)



    #  4. 创建输出文件夹
    os.makedirs("outputs",exist_ok=True)

    #  5. 导出CSV文件
    orders_clean.to_csv("outputs/orders_clean.csv", index=False)
    ad_clean.to_csv("outputs/ad_campaigns_clean.csv", index=False)
    country_metrics = roi_df.merge(
        conversion_df[['country','clicks','conversions','conversion_rate']],
        on="country"
    )
    country_metrics.to_csv("outputs/country_metrics.csv", index=False)

    #  6. 检查清洗后的 DataFrame 是否准备好
    if check_data_ready(orders_clean, ad_clean, country_metrics,verbose=False):
        print("数据清洗和分析已经完成，可以进入后续可视化步骤。")
    else:
        print("数据未准备好，请检查csv文件。")
        return




# 简单行数提示
    print(f"文件已准备好：outputs/orders_clean.csv,outputs/ad_campaigns_clean.csv,outputs/country_metrics.csv")
    print(f"行数示例：orders={len(orders_clean)},ads={len(ad_clean)},country={len(country_metrics)}")

    #  Top 3销售国家
    top_sales_countries = top_n_by_column(orders_clean,'country','sales',3)
    print("Top 3 销售国家：")
    print(top_sales_countries)
    #  Top 3 ROI 国家
    top_roi_countries = top_n_by_column(country_metrics,'country','ROI',3)
    print("Top 3 ROI 国家：")
    print(top_roi_countries)
    #  Top 3 转化率国家
    top_conversion_countries = top_n_by_column(country_metrics,'country','conversion_rate',3)
    print("Top 3 转化率国家：")
    print(top_conversion_countries)

if __name__ == "__main__":
    main()