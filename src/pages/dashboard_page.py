
import streamlit as st
import pandas as pd
import plotly.express as px
from src.services.dashboard_service import build_dashboard_data


def _parse_day_snapshot(day_info, daily_sales_df=None):
    """从 time_metrics 的 best_day/worst_day 中提取展示用日期和销售额。"""
    if not day_info:
        return "暂无数据", 0.0

    if isinstance(day_info, dict):
        raw_date = day_info.get("order_date", "")
        sales = float(day_info.get("sales", 0) or 0)
        clean_date = str(raw_date).split()[0] if raw_date else "暂无数据"
        return clean_date, sales

    clean_date = str(day_info).split()[0]
    sales = 0.0
    if daily_sales_df is not None and not daily_sales_df.empty:
        match_rows = daily_sales_df[
            daily_sales_df["order_date"].astype(str).str.contains(clean_date)
        ]
        if not match_rows.empty:
            sales = float(match_rows["sales"].iloc[0])
    return clean_date, sales


def render_dashboard_page():
    st.subheader("📊 经营看板")

    if "report_data" not in st.session_state:
        st.warning("请先前往【数据同步中心】同步数据")
        st.stop()

    report_data = st.session_state["report_data"]
    dashboard_data = build_dashboard_data(report_data)

    if not dashboard_data.get("success",False):
        st.warning(
            dashboard_data.get("message","看板数据组装失败")
        )
        st.stop()

    core_metrics = report_data.get("core_metrics", {})
    user_metrics = report_data.get("user_metrics", {})

    total_sales = core_metrics.get("total_sales", 0) if isinstance(core_metrics, dict) else 0
    total_orders = core_metrics.get("total_orders", 0) if isinstance(core_metrics, dict) else 0
    avg_order_value = core_metrics.get("avg_order_value", 0) if isinstance(core_metrics, dict) else 0

    # 如果 user_metrics 已经被后端赋成了单纯的 float，就直接用它；如果是标准字典，则提取键值
    if isinstance(user_metrics, dict):
        high_value_ratio = user_metrics.get("high_value_ratio", 0)
    elif isinstance(user_metrics, (int, float)):
        high_value_ratio = user_metrics
    else:
        high_value_ratio = 0

    #  KPI指标
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总销售额：", f"${total_sales:,.2f}")
    col2.metric("订单数量：", f"{int(total_orders)}")
    col3.metric("平均客单价：", f"${avg_order_value:,.2f}")
    col4.metric("高价值用户占比", f"{high_value_ratio:.2%}")

    st.caption(
        f"Top国家：{dashboard_data['best_sales_country']}"
    )

    if dashboard_data["user_health"] == "good":
        st.success(
            "高价值用户贡献较高，用户质量健康。"
        )
    else:
        st.warning(
            "高价值用户占比较低，建议优化用户分层运营。"
        )


    st.subheader("Top3 销售国家")
    st.dataframe(
        dashboard_data["top3_country"],
         use_container_width=True
    )

    st.subheader("销售表现较弱的国家")
    st.dataframe(
        dashboard_data["bottom3_country"],
         use_container_width=True
    )


    #  画国家销售额图表柱状图
    st.subheader("🌍 国家销售分析（动态交互）")
    st.dataframe(
        dashboard_data["country_sales_sorted"],
         use_container_width=True
    )
    country_sales_df = dashboard_data["country_sales_sorted"]

    #  使用 plotly 画柱状图
    fig_country = px.bar(
        country_sales_df,
        x="country",
        y="sales",
        title="Sales by Country",
        labels={"country":"国家","sales":"销售额 ($)"},
        color="sales",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    st.plotly_chart(fig_country, use_container_width=True)


    #  画每日销售趋势折线图
    st.subheader("📈 销售趋势分析(动态交互)")
    daily_sales_df = dashboard_data["daily_sales"]

    if daily_sales_df.empty:
        st.info(
            "暂无销售趋势数据"
        )
    else:
        daily_sales_df['order_date'] = pd.to_datetime(daily_sales_df['order_date']).dt.date

        fig_trend = px.line(
            daily_sales_df,
            x="order_date",
            y="sales",
            title="Daily Sales Trend",
            labels={"order_date":"日期","sales":"销售额 ($)"},
            markers=True,
            template="plotly_white"
        )

        fig_trend.update_xaxes(
            type='category',
            tickangle=-45
        )

        st.plotly_chart(fig_trend, use_container_width=True)


    #  === 结尾写一个分析报告 ===
    st.markdown("---")
    st.subheader("🤖 图表联动 · AI智能深度诊断")
    st.caption("以下是基于上方图表自动生成的异动特征，点击按钮可直接联动【AI经营顾问】进行深度原因分析。")

    best_day = dashboard_data["best_day"]
    worst_day = dashboard_data["worst_day"]
    best_sales_country = dashboard_data["best_sales_country"]
    best_country_sales = dashboard_data["best_country_sales"]



    #  使用卡片式布局展示核心异动，并绑定一键联动按钮
    col_a ,col_b = st.columns(2)

    with col_a:
        with st.container(border=True):
            st.markdown("🌍 市场表现异动")
            st.markdown(f"**销售额最高的国家：** '{best_sales_country}'")
            st.markdown(f"**累计销售总额：** '${best_country_sales:,.1f}'")
            # 留白对齐高度
            st.markdown("<br>", unsafe_allow_html=True)
            # 联动按钮：点击后问题将注入 session_state
            if st.button(f"🔍 深度诊断{best_sales_country}市场",key="link_country_ai"):
                st.session_state["input_question"] = f"帮我深度分析一下{best_sales_country}市场的表现，为什么它销售额最高？有那些增长点和潜在风险？"
                st.info("💡 诊断请求已提交！请点击切换到【💬 AI经营顾问】页面查看深度分析报告。")

    with col_b:
        with st.container(border=True):
            # 右侧：趋势波动维度（严格按照你要求的“波峰出现在”格式格式化数值）
            st.markdown("### 📈 销售趋势异动")

            clean_best_day, best_day_sales = _parse_day_snapshot(best_day, daily_sales_df)
            clean_worst_day, worst_day_sales = _parse_day_snapshot(worst_day, daily_sales_df)

            st.markdown(f"每日销售额波峰出现在：{clean_best_day}，${best_day_sales:,.2f}")
            st.markdown(f"每日销售额波谷出现在：{clean_worst_day}，${worst_day_sales:,.2f}")


            st.markdown("<br>", unsafe_allow_html=True)



            # 联动按钮
            if st.button(f"📊 分析{clean_best_day}销量暴涨原因",key="link_trend_ai",use_container_width=True):
                st.session_state["input_question"] = f"从销售趋势图来看，为什么{clean_best_day}这一天的销售额达到了波峰${best_day_sales:.2f}，而{clean_worst_day}掉到了波谷${worst_day_sales:.2f}."
                st.info("💡 诊断请求已提交！请点击切换到【💬 AI经营顾问】页面查看深度分析报告。")
        #  保留原本基础业务洞察作为文本底座，方便用户对比
    with st.expander("📄 查看看板基础统计明确"):
        st.write(f"1. {best_sales_country} 是当前销售额最高的国家，销售额为 ${best_country_sales:,.2f}。")
        st.write(
            f"2. 销售额最高的日期是 {clean_best_day}（${best_day_sales:,.2f}），"
            f"销售额最低的日期是 {clean_worst_day}（${worst_day_sales:,.2f}）。"
        )
