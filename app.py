

import streamlit as st
from src.pages.sync_page import render_sync_page
from src.pages.dashboard_page import render_dashboard_page
from src.pages.report_page import render_report_page
from src.pages.consultant_page import render_consultant_page


# 接下来是你原有的标签页布局定义（位置对齐）
tab1, tab2, tab3 ,tab4 = st.tabs([
    "📥 数据同步中台",
    "📊 动态智能看板",
    "🤖 AI 战略诊断报告",
    "💬 AI经营顾问"
])

with tab1:
    render_sync_page()

with tab2:
    render_dashboard_page()

with tab3:
    render_report_page()

with tab4:
    render_consultant_page()



















