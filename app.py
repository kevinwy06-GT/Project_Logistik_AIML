import streamlit as st
import pandas as pd

from services.optimization_service import OptimizationService

st.set_page_config(
    page_title="Logistics Optimization System",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Logistics Optimization System")
st.markdown(
    """
This application optimizes freight allocation using:

- 🧬 Genetic Algorithm
- 🔥 Simulated Annealing
"""
)

st.divider()

# ==========================================================
# RUN BUTTON
# ==========================================================

if st.button("🚀 Run Optimization", use_container_width=True):

    with st.spinner("Running Genetic Algorithm..."):

        service = OptimizationService()

        result = service.optimize()

    st.success("Optimization Finished!")

    st.divider()

    # ======================================================
    # FITNESS HISTORY
    # ======================================================

    st.subheader("GA Fitness History")

    fitness_df = pd.DataFrame({
        "Generation": list(range(1, len(result.fitness_history)+1)),
        "Fitness": result.fitness_history
    })

    st.line_chart(
        fitness_df.set_index("Generation")
    )

    st.divider()

    # ======================================================
    # TRUCK ASSIGNMENT
    # ======================================================

    st.subheader("Truck Allocation")

    for truck_name, goods in result.truck_assignments.items():

        with st.expander(truck_name, expanded=True):

            if len(goods) == 0:

                st.info("No goods assigned.")

            else:

                df = pd.DataFrame([
                    {
                        "Item ID": item.item_id,
                        "Item": item.item_name,
                        "Destination": item.destination_city,
                        "Weight": item.weight_kg,
                        "Volume": item.volume_m3
                    }
                    for item in goods
                ])

                st.dataframe(
                    df,
                    use_container_width=True
                )

    st.divider()

    # ======================================================
    # ROUTES
    # ======================================================

    st.subheader("Optimized Routes")

    for truck_name, route in result.routes.items():

        st.write(f"### {truck_name}")

        if len(route) == 0:

            st.info("No destination.")

        else:

            st.write(
                " → ".join(
                    ["Surabaya"] +
                    route +
                    ["Surabaya"]
                )
            )

    st.divider()

    # ======================================================
    # REJECTED GOODS
    # ======================================================

    st.subheader("Rejected Goods")

    if len(result.rejected_goods) == 0:

        st.success("No rejected goods.")

    else:

        rejected_df = pd.DataFrame([
            {
                "Item ID": item.item_id,
                "Item": item.item_name,
                "Destination": item.destination_city,
                "Weight": item.weight_kg
            }
            for item in result.rejected_goods
        ])

        st.dataframe(
            rejected_df,
            use_container_width=True
        )

else:

    st.info("Click **Run Optimization** to start.")