
import streamlit as st
import re
from src.agent import route_question
from src.llm_explainer import explain_result_stream

def render_consultant_page():
    st.subheader("💬 AI经营顾问")
    if "report_data" not in st.session_state:
        st.warning("请先前往【数据同步中心】同步数据")
        return

    # 注入自定义 CSS，优雅解决 st.metric 字体过大导致的截断、换行和显示不全问题
    st.markdown("""
        <style>
        [data-testid="stMetricLabel"] {
            font-size: 16px !important;
            font-weight: 600 !important;
            color: #333333 !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 22px !important;
            word-break: break-all !important;
            white-space: normal !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ✅ 新增：调试信息，确认数据是否正确传入
    with st.expander("🔧 数据状态检查"):
        st.write("country_metrics_df:",
                 st.session_state.get("country_metrics_df") is not None)
        st.write("roi_df:",
                 st.session_state.get("roi_df") is not None)
        st.write("daily_sales:",
                 st.session_state.get("daily_sales") is not None)
        st.write("orders_df:",
                 st.session_state.get("orders_df") is not None)



    # 核心联动：初始化输入框缓存
    if "input_question" not in st.session_state:
        st.session_state["input_question"] = ""
    # 接收来自Tab2传递过来的联动问题
    current_placeholder = "例如：哪个国家的销售额最高？"
    if st.session_state["input_question"]:
        st.info(f"已自动载入来自【经营看板】图表的联动诊断请求：\n'{st.session_state['input_question']}'")

    # 绑定value ,当用户在画布点击联动时，这里的输入框内容会自动被改写
    question = st.text_input(
        "请输入你的经营问题",
        value=st.session_state["input_question"],
        placeholder=current_placeholder,
        key="question_widget"
    )


    if st.button("开始分析"):
        if not question.strip():
            st.warning(
                "请输入经营问题"
            )
            return

        with st.spinner("AI 分析中..."):

            tool_result = route_question(
                question,
                country_df=st.session_state.get("country_metrics_df"),
                roi_df=st.session_state.get("roi_df"),
                daily_df=st.session_state.get("daily_sales"),
                orders_df=st.session_state.get("orders_df")
            )

            raw_score = tool_result.get("score", 0)
            try:
                numeric_score = float(raw_score)
                numeric_score = round(numeric_score, 2)
            except (ValueError, TypeError):
                numeric_score = 0


            #  将规范化之后的分数写回到tool_result中
            tool_result["score"] = numeric_score
            formatted_score = f"{numeric_score}%"

            intent = tool_result.get("intent", "未知意图")
            tool_name = tool_result.get("tool", "未匹配到工具")


            # 2：采用分栏KPI卡片显示
            with st.expander("Agent链路决策日志",expanded=True):
                col1,col2,col3 = st.columns(3)
                with col1:
                    st.metric(label="识别业务意图",value=intent)
                with col2:
                    # 根据分数动态改变置信度颜色提示
                    if numeric_score >= 90:
                        st.metric(label="意图匹配置信度",value=formatted_score,delta="高置信度")
                    elif numeric_score >= 80:
                        st.metric(label="意图匹配置信度",value=formatted_score,delta="中置信度",delta_color="off")
                    else:
                        st.metric(label="意图匹配置信度",value=formatted_score,delta="低置信度",delta_color="inverse")

                with col3:
                    # 美化工具名称展示，去掉下划线并转化为首字母大写
                    clean_tool_name = str(tool_name).replace("_"," ").title()
                    st.metric(label="路由调用工具",value=clean_tool_name)


            # 把原油JSON塞进二级折叠栏
            with st.expander("查看底层工具元数据"):
                st.json(tool_result)

            # 升级为商业状态横条
            if numeric_score >= 90:
                st.success("Agent成功锁定高可信度执行路径，正在交由AI经营顾问进行深入分析")
            elif numeric_score >= 80:
                st.info("Agent已在标准路径下响应")
            else:
                st.warning("匹配的置信度较低，建议提问时带上更明确的跨境业务关键词（如“国家”，“销售额”等）")

            # 4. 后续业务数据分析与解释逻辑
            if not tool_result.get("success", False):
                st.error(tool_result.get("message", "执行失败"))
                if "last_answer" in st.session_state:
                    del st.session_state["last_answer"]
            else:
                # 调用 llm_explainer 模块进行大白话解读
                # 打字机式流式输出
                st.markdown("___")
                st.markdown("AI经营顾问建议")
                with st.chat_message("assistant",avatar="💬"):
                    full_answer = st.write_stream(explain_result_stream(question,tool_result))

                st.session_state["last_answer"] = full_answer
                st.session_state["last_question"] = question
                #  只渲染一次
                st.session_state["just_streamed"] = True
                st.rerun()


    # 结果与下载区域，保持在按钮外部
    if "last_answer" in st.session_state and st.session_state["last_answer"] is not None:
        if not st.session_state.get("just_streamed",False):
            st.markdown("___")
            st.markdown("## AI经营顾问建议(折叠面板展示)")
            # with st.chat_message("assistant",avatar="💬"):
            #    st.markdown(st.session_state["last_answer"])
            ai_report = st.session_state["last_answer"]

            # 使用更标准的 Markdown 标题（### ）进行动态段落切分
            sections = re.findall(r"###\s+([^\n]+)\n([^#]*)", ai_report, re.DOTALL)

            if not sections:
                # 兜底方案：如果没有匹配到标准化标题，直接用完整的卡片包起来
                with st.expander("📋 查看完整经营建议报告", expanded=True):
                    st.markdown(ai_report)
            else:
                # 动态循环生成折叠面板，结构和你的战略报告完全对齐
                for title_inner, content_inner in sections:
                    with st.expander(f"📌 {title_inner.strip()}", expanded=True):
                        st.markdown(content_inner.strip())
        else:
            # 重置标志位
            st.session_state["just_streamed"] = False

        file_name = f"AI经营建议_{st.session_state.get('last_question')}.md"
        st.download_button(
            label="一键下载AI经营建议（markdown格式）",
            data=st.session_state["last_answer"],
            file_name = file_name,
            mime="text/markdown",
            key="download_advice_btn"
        )