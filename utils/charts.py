"""
charts.py

Reusable charts for the dashboard.
"""

import pandas as pd
import streamlit as st


def show_truck_utilization(result):

    st.subheader("🚚 Truck Utilization")

    if not result.truck_utilization:
        st.info("No utilization data available.")
        return

    df = pd.DataFrame({
        "Truck": list(result.truck_utilization.keys()),
        "Utilization (%)": list(result.truck_utilization.values())
    })

    st.bar_chart(
        df.set_index("Truck")
    )


def show_truck_profit(result):

    st.subheader("💰 Profit by Truck")

    if not result.truck_profit:
        st.info("No profit data available.")
        return

    df = pd.DataFrame({
        "Truck": list(result.truck_profit.keys()),
        "Profit": list(result.truck_profit.values())
    })

    st.bar_chart(
        df.set_index("Truck")
    )


def show_truck_distance(result):

    st.subheader("📏 Distance by Truck")

    if not result.truck_distance:
        st.info("No distance data available.")
        return

    df = pd.DataFrame({
        "Truck": list(result.truck_distance.keys()),
        "Distance (km)": list(result.truck_distance.values())
    })

    st.bar_chart(
        df.set_index("Truck")
    )
