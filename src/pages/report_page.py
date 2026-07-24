
import re
import streamlit as st
from src.services.ai_report_service import (
get_data_hash,
generate_ai_report_stream
)


def render_report_page():
    st.subheader("🧠 AI 战略分析")
    if "report_data" not in st.session_state:
        st.warning("⚠️ 请先前往【数据同步中心】同步数据")
        st.stop()

    report_data = st.session_state["report_data"]
    data_hash = get_data_hash(report_data)

    column1, column2 = st.columns(2)

    with column1:
        generate_clicked = st.button(
            "🚀 生成AI分析报告"
        )
    with column2:
        regen_clicked = st.button(
            "🔄 重新生成报告"
        )
    if regen_clicked:
        st.session_state.pop("ai_report", None)
        st.session_state.pop("data_hash", None)
        generate_clicked = True

    cache_valid = (
        "ai_report" in st.session_state
        and st.session_state.get("data_hash") == data_hash
    )

    if generate_clicked :
        if cache_valid :
            st.info("数据未变化，已使用缓存报告。如需刷新请点击【重新生成报告】")
        else:
            try:
                placeholder = st.empty()
                full_report = ""

                status = st.status(
                    "AI正在生成战略报告...",
                    expanded=True
                )

                with status:
                    for chunk in generate_ai_report_stream(report_data):
                        full_report += chunk
                        placeholder.markdown(full_report)
                    status.update(
                        label="报告生成完毕！",
                        state="complete"
                    )
                st.session_state["ai_report"] = full_report
                st.session_state["data_hash"] = data_hash
                st.rerun()


            except Exception as e:

                st.error("AI生成失败，请检查网络或稍后重试")

                st.text(str(e))

                # 👇 加这一行，把真正的错误打在 PowerShell 终端里，方便看看到底是不是网络超时

                import traceback;
                traceback.print_exc()

    # 👉 只要有缓存，就显示报告（不需要再点按钮）
    if "ai_report" in st.session_state:
        ai_report = st.session_state["ai_report"]
        st.markdown("## 📊 AI 战略分析报告（咨询级）")
        # 🔥 终极修正：利用 .get() 确保无论如何重载，绝对不爆 KeyError
        core_box = report_data.get('core_metrics', {})
        s_val = core_box.get('total_sales', 0.0)
        o_val = core_box.get('total_orders', 0)
        a_val = core_box.get('avg_order_value', 0.0)
        columns1, columns2, columns3 = st.columns(3)
        columns1.metric("总销售额", f"${s_val:.2f}")
        columns2.metric("订单数", f"{o_val} 笔")
        columns3.metric("客单价", f"${a_val:.2f}")

        st.success("报告已生成（已缓存，下次秒开）")

        #  通用动态切分

        sections = re.findall(
            r"【([^】]+)】([^【]*)",
            ai_report,
            re.DOTALL
        )

        if not sections:
            st.markdown(ai_report)
        else:
            for title_inner,content in sections:
                title = f"【{title_inner}"
                expanded = any(
                    k in title for k in ["摘要","——"]
                )

                with st.expander(title,expanded=expanded):
                        st.markdown(content.strip())

        st.download_button(
            label="📥 下载报告",
            data=ai_report.encode("utf-8"),
            file_name="AI_Strategy_Report.txt",
            mime="text/plain; charset=utf-8"
        )
    else:
        st.info("👉 点击按钮生成AI分析报告")

