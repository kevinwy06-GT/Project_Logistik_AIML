"""
dashboard_page.py

Main Dashboard Page.
"""

import streamlit as st
import pandas as pd

from utils.dashboard_components import (
    executive_summary,
    simulated_annealing_summary,
)

from utils.dashboard_tables import (
    truck_assignment_table,
    route_table,
    rejected_goods_table,
)

from utils.charts import (
    show_truck_utilization,
    show_truck_profit,
    show_truck_distance,
)


def show():

    st.title("📊 Optimization Dashboard")

    if "optimization_result" not in st.session_state:

        st.warning(
            "No optimization has been run yet.\n\n"
            "Go to the Optimization page first."
        )

        return

    result = st.session_state["optimization_result"]

    # ==========================================================
    # Executive Summary
    # ==========================================================

    executive_summary(result)

    st.divider()

    # ==========================================================
    # Simulated Annealing Summary
    # ==========================================================

    simulated_annealing_summary(result)

    st.divider()

    # ==========================================================
    # Fitness History
    # ==========================================================

    st.subheader("📈 Fitness History")

    history = pd.DataFrame(
        {
            "Generation": range(
                1,
                len(result.fitness_history) + 1
            ),
            "Fitness": result.fitness_history,
        }
    )

    st.line_chart(
        history.set_index("Generation")
    )

    st.divider()

    # ==========================================================
    # Charts
    # ==========================================================

    show_truck_utilization(result)

    st.divider()

    show_truck_profit(result)

    st.divider()

    show_truck_distance(result)

    st.divider()

    # ==========================================================
    # Tables
    # ==========================================================

    truck_assignment_table(result)

    st.divider()

    route_table(result)

    st.divider()

    rejected_goods_table(result)
