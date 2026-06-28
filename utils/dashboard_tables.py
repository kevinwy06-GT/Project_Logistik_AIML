"""
dashboard_tables.py

Reusable dashboard tables.
"""

import pandas as pd
import streamlit as st


def truck_assignment_table(result):

    st.subheader("🚚 Truck Assignments")

    for truck, goods in result.truck_assignments.items():

        with st.expander(truck, expanded=True):

            truck_id = truck.replace("Truck ", "TRK-0")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Weight",
                f"{result.truck_weight.get(truck_id,0):,.0f} kg"
            )

            col2.metric(
                "Volume",
                f"{result.truck_volume.get(truck_id,0):,.1f} m³"
            )

            col3.metric(
                "Utilization",
                f"{result.truck_utilization.get(truck_id,0):.1f}%"
            )

            if len(goods) == 0:

                st.info("No goods assigned.")

                continue

            rows = []

            for item in goods:

                rows.append({
                    "Item ID": item.item_id,
                    "Item": item.item_name,
                    "Destination": item.destination_city,
                    "Weight": item.weight_kg,
                    "Volume": item.volume_m3,
                })

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True
            )


def route_table(result):

    st.subheader("🗺 Optimized Routes")

    for truck, route in result.routes.items():

        st.markdown(f"### {truck}")

        if len(route) == 0:

            st.info("No destination.")

            continue

        st.success(
            " ➜ ".join(
                ["Surabaya"] +
                route +
                ["Surabaya"]
            )
        )


def rejected_goods_table(result):

    st.subheader("❌ Rejected Goods")

    if len(result.rejected_goods) == 0:

        st.success("No rejected goods.")

        return

    rows = []

    for item in result.rejected_goods:

        rows.append({
            "Item ID": item.item_id,
            "Item": item.item_name,
            "Destination": item.destination_city,
            "Weight": item.weight_kg,
            "Volume": item.volume_m3,
        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )
