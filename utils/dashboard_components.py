"""
dashboard_components.py

Reusable dashboard UI components.
"""

import streamlit as st


def executive_summary(result):
    """Display executive summary cards."""

    st.subheader("📈 Executive Summary")

    row1 = st.columns(4)

    row1[0].metric(
        "Net Profit",
        f"Rp {result.net_profit:,.0f}"
    )

    row1[1].metric(
        "Revenue",
        f"Rp {result.total_revenue:,.0f}"
    )

    row1[2].metric(
        "Operating Cost",
        f"Rp {result.total_operating_cost:,.0f}"
    )

    row1[3].metric(
        "Toll Cost",
        f"Rp {result.total_toll_cost:,.0f}"
    )

    row2 = st.columns(4)

    row2[0].metric(
        "Distance",
        f"{result.total_distance:.1f} km"
    )

    row2[1].metric(
        "Rejected Goods",
        len(result.rejected_goods)
    )

    row2[2].metric(
        "Generations",
        result.generations
    )

    row2[3].metric(
        "Best Fitness",
        f"{result.best_chromosome.fitness:,.2f}"
    )


def simulated_annealing_summary(result):
    """Display SA improvement summary."""

    st.subheader("🔥 Simulated Annealing Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Before SA",
        f"{result.before_sa_distance:.1f} km"
    )

    col2.metric(
        "After SA",
        f"{result.after_sa_distance:.1f} km"
    )

    col3.metric(
        "Distance Saved",
        f"{result.distance_saved:.1f} km"
    )
