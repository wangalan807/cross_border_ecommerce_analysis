


#  Tool1 销售额最高的国家
def get_top_sales_country(country_df):
    if country_df is None:
        return {
            "success": False,
            "message": "country_df不存在"
        }
    if country_df.empty or "sales" not in country_df.columns:
        return {"success": False,"message":"country_df为空或缺少'sales'列"}

    try:
        row = country_df.loc[
            country_df["sales"].idxmax()
    ]
    except ValueError:
        return {"success":False,"message":"所有销售额为NaN"}
    return {
        "success": True,
        "tool":"top_sales_country",
        "data":{ "country":row["country"],"sales":float(row["sales"])}
    }

#  Tool2 销售额最低的国家
def get_bottom_sales_country(country_df):
    if country_df is None:
        return {
            "success": False,
            "message": "country_df不存在"
        }
    if country_df.empty or "sales" not in country_df.columns:
        return {"success": False,"message":"country_df为空或缺少'sales'列"}
    try:
        row = country_df.loc[
            country_df["sales"].idxmin()
        ]
    except ValueError:
        return {"success": False, "message": "所有销售额为NaN"}
    return {
        "success": True,
        "tool": "bottom_sales_country",
        "data": {"country": row["country"], "sales": float(row["sales"])}
    }


#  Tool3 ROI最高的国家
def get_top_roi_country(roi_df):
    if roi_df is None:
        return {
            "success": False,
            "message": "roi_df不存在"
        }
    if roi_df.empty:
        return {"success": False,"message":"roi_df为空"}
    if "ROI" in roi_df.columns:
        roi_col = "ROI"
    elif "roi" in roi_df.columns:
        roi_col = "roi"
    else:
        return {
            "success": False,
            "message":"未找到ROI列"
        }
    df = roi_df.dropna(subset=[roi_col])
    #  更改列名后再判断
    if df.empty:
        return {"success":False,"message":"ROI列为全空"}
    row = df.loc[
        df[roi_col].idxmax()
    ]
    return {
        "success": True,
        "tool":"top_roi_country",
        "data":{"country":row["country"],"ROI":float(row[roi_col])}
    }

#  Tool4 ROI最低的国家
def get_lowest_roi_country(roi_df):
    if roi_df is None:
        return {
            "success": False,
            "message": "roi_df不存在"
        }
    if roi_df.empty:
        return {"success": False, "message": "roi_df为空"}
    if "ROI" in roi_df.columns:
        roi_col = "ROI"
    elif "roi" in roi_df.columns:
        roi_col = "roi"
    else:
        return {
            "success": False,
            "message": "未找到ROI列"
        }
    df = roi_df.dropna(subset=[roi_col])
    #  更改列名后再判断
    if df.empty:
        return {"success": False, "message": "ROI列为全空"}
    row = df.loc[
        df[roi_col].idxmin()
    ]
    return {
        "success": True,
        "tool": "lowest_roi_country",
        "data": {"country": row["country"], "ROI": float(row[roi_col])}
    }


#  Tool5 销售额最好的一天
def get_best_sales_day(daily_df):
    if daily_df is None:
        return {
            "success": False,
            "message": "daily_df不存在"
        }
    required_cols = ["order_date","sales"]
    if daily_df.empty or any(col not in daily_df.columns for col in required_cols):
        return {"success":False,"message":"daily_df为空或缺少必要列"}
    df = daily_df.dropna(subset=["sales"])
    if df.empty:
        return {"success":False,"message":"sales列全为空"}
    row = df.loc[
        df["sales"].idxmax()
    ]
    return {
        "success": True,
        "tool":"best_sales_day",
        "data":{"date":str(row["order_date"]), "sales":float(row["sales"])}
    }

#  Tool6 销售额最差的一天
def get_worst_sales_day(daily_df):
    if daily_df is None:
        return {
            "success": False,
            "message": "daily_df不存在"
        }
    required_cols = ["order_date", "sales"]
    if daily_df.empty or any(col not in daily_df.columns for col in required_cols):
        return {"success": False, "message": "daily_df为空或缺少必要列"}
    df = daily_df.dropna(subset=["sales"])
    if df.empty:
        return {"success": False, "message": "sales列全为空"}
    row = df.loc[
        df["sales"].idxmin()
    ]
    return {
        "success": True,
        "tool": "worst_sales_day",
        "data": {"date": str(row["order_date"]), "sales": float(row["sales"])}
    }
#  Tool7 高价值用户分析
HIGH_VALUE_LABEL = "High Value"

def get_high_value_user_stats(orders_df):
    if orders_df is None:
        return {
            "success": False,
            "message": "orders_df不存在"
        }

    if orders_df.empty or "user_id" not in orders_df.columns or "user_value_segment" not in orders_df.columns:
        return {"success":False,"message":"缺少必要列或DataFrame为空"}
    total_users = orders_df["user_id"].nunique()
    high_users = orders_df[orders_df["user_value_segment"] == HIGH_VALUE_LABEL
    ]["user_id"].nunique()

    ratio = high_users / total_users if total_users else 0
    return {
        "success": True,
        "tool":"high_value_user_stats",
        "data":{"total_users":int(total_users),"high_value_users":int(high_users),"ratio":round(ratio,4)}
    }


#  Tool8 广告预算推荐

def get_ad_candidates(country_df):


    if country_df is None:
        return {
            "success": False,
            "message": "country_df不存在"
        }
    if country_df.empty:
        return {"success":False,"message":"country_df为空","data":[]}
    #roi_col = "ROI" if "ROI" in country_df.columns else "roi"
    if "ROI" in country_df.columns:
        roi_col = "ROI"
    elif "roi" in country_df.columns:
        roi_col = "roi"
    else:
        return {
            "success": False,
            "message":"未找到ROI列",
            "data":[]
        }
    if "conversion_rate" not in country_df.columns:
        return {"success":False,"message":"缺少conversion_rate列","data":[]}
    avg_roi = country_df[roi_col].mean()
    avg_conversion_rate = country_df["conversion_rate"].mean()

    result = country_df[
        (country_df[roi_col] > avg_roi)
        &
        (country_df["conversion_rate"] > avg_conversion_rate)
    ]
    countries = result["country"].tolist() if not result.empty else []

    output = result[
        [
            "country",
            roi_col,
            "conversion_rate",
            "sales"
        ]
    ]
    return {
        "success": True,
        "tool":"ad_candidates",
        "summary": countries,
        "data": output.to_dict("records")
        }


