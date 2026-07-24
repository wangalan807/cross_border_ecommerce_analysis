
import streamlit as st
from src.services.sync_mysql_service import sync_mysql_service




def render_sync_page():
    st.subheader("📂 生产环境数据库实时同步")
    st.info("当前已配置直连本地 MySQL 数据库: 'cross_border_ecommerce_db'")

    if st.button("实时同步MYSQL数据库并触发AI诊断"):
        with st.spinner(
            "正在建立安全的数据库连接..."
        ):
            result = sync_mysql_service()

        if not result or not result.get("success",False):
            error_reason = result.get("message") or result.get("error","未知的数据流清洗中断")
            st.error(f"数据同步失败，原因：{error_reason}")
            st.warning("温馨提示：通常因为计算漏洞或数据库连接错误")
            return

        sales_outliers = result.get("sales_outliers",[])
        st.metric("异常订单数",len(sales_outliers))

        st.session_state["orders_df"] = result.get("orders_df")
        st.session_state["country_metrics_df"] = result.get("country_metrics_df")
        st.session_state["daily_sales"] = result.get("daily_sales_df")
        st.session_state["roi_df"] = result.get("roi_df")
        # 兼容大模型报告结构
        st.session_state["report_data"] = result

        # 清理旧缓存
        st.session_state.pop("ai_report",None)
        st.session_state.pop("data_hash",None)
        st.success("MYSQL生产数据同步成功！")


        # 清理旧的AI缓存
        if "ai_report" in st.session_state:
            del st.session_state["ai_report"]

        st.success(
            "🎉 MySQL生产数据同步成功,500条大样本数据全部清洗完成！"
            )

        st.toast(
            "数据管道同步成功！",
            icon="🚀"
            )




    st.subheader("小提示：")
    st.info("Tab1=数据同步")
    st.info("Tab2=数据看板")
    st.info("Tab3=AI战略报告")
    st.info("Tab4=AI经营顾问")