import streamlit as st

from ui.home_page import show as home_page
from ui.goods_page import show as goods_page
from ui.optimization_page import show as optimization_page
from ui.dashboard_page import show as dashboard_page
from ui.truck_page import show as truck_page

st.set_page_config(
    page_title="Logistics Optimization System",
    page_icon="🚚",
    layout="wide"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📦 Goods",
        "🚚 Trucks",
        "🧬 Optimization",
        "📊 Dashboard"
    ]
)

if page == "🏠 Home":
    home_page()

elif page == "📦 Goods":
    goods_page()

elif page == "🚚 Trucks":

    truck_page()

elif page == "🧬 Optimization":
    optimization_page()

elif page == "📊 Dashboard":
    dashboard_page()