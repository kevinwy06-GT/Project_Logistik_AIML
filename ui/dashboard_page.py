import streamlit as st
import pandas as pd


def show():

    st.title("📊 Optimization Dashboard")

    if "optimization_result" not in st.session_state:

        st.warning(
            "No optimization has been run yet.\n\nGo to the Optimization page first."
        )

        return

    result = st.session_state["optimization_result"]

    # ====================================================
    # TOP METRICS
    # ====================================================

    st.subheader("Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Generations",
        result.generations
    )

    col2.metric(
        "Best Fitness",
        f"{result.best_chromosome.fitness:,.2f}"
    )

    col3.metric(
        "Rejected Goods",
        len(result.rejected_goods)
    )

    st.divider()

    # ====================================================
    # FITNESS HISTORY
    # ====================================================

    st.subheader("Fitness History")

    history = pd.DataFrame(
        {
            "Generation": range(
                1,
                len(result.fitness_history) + 1
            ),
            "Fitness": result.fitness_history
        }
    )

    st.line_chart(
        history.set_index("Generation")
    )

    st.divider()

    # ====================================================
    # TRUCK ASSIGNMENTS
    # ====================================================

    st.subheader("Truck Assignments")

    for truck, goods in result.truck_assignments.items():

        with st.expander(truck, expanded=True):

            if len(goods) == 0:

                st.info("No goods assigned.")

                continue

            table = []

            for item in goods:

                table.append(
                    {
                        "Item ID": item.item_id,
                        "Item": item.item_name,
                        "Destination": item.destination_city,
                        "Weight": item.weight_kg,
                        "Volume": item.volume_m3,
                    }
                )

            st.dataframe(
                pd.DataFrame(table),
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    # ====================================================
    # ROUTES
    # ====================================================

    st.subheader("Optimized Routes")

    for truck, route in result.routes.items():

        st.markdown(f"### {truck}")

        if len(route) == 0:

            st.info("No destination.")

        else:

            st.success(
                " ➜ ".join(
                    ["Surabaya"] + route + ["Surabaya"]
                )
            )

    st.divider()

    # ====================================================
    # REJECTED GOODS
    # ====================================================

    st.subheader("Rejected Goods")

    if len(result.rejected_goods) == 0:

        st.success("No rejected goods.")

    else:

        table = []

        for item in result.rejected_goods:

            table.append(
                {
                    "Item ID": item.item_id,
                    "Item": item.item_name,
                    "Destination": item.destination_city,
                    "Weight": item.weight_kg,
                }
            )

        st.dataframe(
            pd.DataFrame(table),
            use_container_width=True,
            hide_index=True
        )