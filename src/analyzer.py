
import pandas as pd




# 新增一个时间转换函数
def convert_order_date(df):
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

# 写一个增加销售额列
def add_sales_column(df):
    df["sales"] = (df["unit_price"] * df["quantity"])
    return df

#  写一个时间特征函数
def add_time_features(df):
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_week"] = df["order_date"].dt.isocalendar().week
    return df

def get_country_sales(df):

    country_sales = (
        df.groupby("country")["sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="sales",
            ascending=False
        )
    )
    return country_sales

def calculate_roi(country_sales, ad_df):
    ad_by_country = (
        ad_df.groupby("country", as_index=False)
        .agg(
            ad_cost=("ad_cost", "sum"),
            clicks=("clicks", "sum"),
            conversions=("conversions", "sum"),
        )
    )
    safe_clicks = ad_by_country["clicks"].replace(0, pd.NA)
    ad_by_country["conversion_rate"] = (
        ad_by_country["conversions"] / safe_clicks * 100
    ).fillna(0)

    roi_df = pd.merge(country_sales, ad_by_country, on="country")
    safe_ad_cost = roi_df["ad_cost"].replace(0, pd.NA)
    roi_df["ROI"] = (roi_df["sales"] / safe_ad_cost).fillna(0)

    roi_df = roi_df.sort_values(by="ROI", ascending=False)
    return roi_df

def add_conversion_rate(ad_df):
    ad_df = ad_df.copy()
    if "conversion_rate" not in ad_df.columns:
        ad_df["conversion_rate"] = (ad_df["conversions"] / ad_df["clicks"] *100)
        ad_df = ad_df.sort_values(
            by="conversion_rate",
            ascending=False
    )
    return ad_df

# 写一个获取每日销售额趋势的函数，冰花折线图
def get_daily_sales(df):
    return (
        df.groupby("order_date")["sales"]
        .sum()
        .reset_index()
    )

# 写一个用户分析
def get_top_users(df):
    user_sales = (
        df.groupby("user_id")["sales"].sum().sort_values(ascending=False)
    )
    return user_sales

#  写一个用户价值分段
def add_user_value_segment(df):
    user_total_sales = df.groupby("user_id")["sales"].sum()
    threshold = user_total_sales.quantile(0.8)

    df["user_value_segment"] = df["user_id"].map(
        lambda user_id: "High Value"
        if user_total_sales[user_id] >=  threshold
        else "Normal Value"
    )
    return df


# 写一个kpi分析
def get_kpi_metrics(df,country_sales,roi_df,conversion_df):
    total_sales = df["sales"].sum()
    top_sales_country = country_sales.loc[
        country_sales["sales"].idxmax(),
        "country"
    ]
    avg_roi = round(roi_df["ROI"].mean(),2)
    best_conversion_rate_country = conversion_df.loc[
        conversion_df["conversion_rate"].idxmax(),
        "country"
    ]

    return {
        "total_sales":total_sales,
        "top_sales_country":top_sales_country,
        "avg_roi":avg_roi,
        "best_conversion_rate_country":best_conversion_rate_country
    }


#  新增一个数据检查函数
def check_data_ready(orders_clean,ad_clean,country_metrics,verbose=False):
    """
    检查数据清晰和分析结果是否有用。
    检查内容：
    1. DataFrame是否为空。
    2. 是否存在缺失值。
    3. 是否存在重复值。
    """
    dataframes = {
        "orders_clean":orders_clean,
        "ad_clean":ad_clean,
        "country_metrics":country_metrics
    }
    all_ready = True

    for name,df in dataframes.items():


        if df.empty:
            print(f"{name} 数据为空")
            all_ready = False
            continue

        missing_values = df.isna().sum()
        duplicate_count = df.duplicated().sum()


        if verbose:
            print(f"\n=== 检查 {name} ===")

            print(f"{name} 行数：{len(df)}")
            print(f"{name} 列名：{list(df.columns)}")

            print("缺失值统计：")
            print(missing_values)

            print(f"重复行数量：{duplicate_count}")

        if missing_values.sum() > 0:
            print(f"{name} 存在缺失值")
            all_ready = False

        if duplicate_count > 0:
            print(f"{name} 存在重复行")
            all_ready = False

    return all_ready


#  写一个检测异常值函数
def detect_outliers(df,column,method='iqr'):
    """
    检测指定列的异常值
    df： pandas DataFrame
    column:要检查的列名。例如：‘sales’
    method:'iqr'或'zscore'
    返回异常值的DataFrame
    """
    if method == 'iqr':
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        IQR = q3 - q1
        lower_bound = q1 - 1.5 *IQR
        upper_bound = q3 + 1.5 * IQR

    elif method == 'zscore':
        mean = df[column].mean()
        std = df[column].std()
        lower_bound = mean - 3 * std
        upper_bound = mean + 3 * std

    else:
        raise ValueError("method 必须是 'iqr' 或 'zscore'")

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers


#  写一个按列排序函数
def top_n_by_column(df,group_column,target_column,n=3):
    """
    按target_column排序，返回 Top N 的 group_column
    """
    summary = df.groupby(group_column)[target_column].sum().reset_index()
    top_n = summary.sort_values(by=target_column,ascending=False).head(n)
    return top_n


