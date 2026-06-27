import streamlit as st
import pandas as pd

from services.optimization_service import OptimizationService


def show():

    st.title("🧬 Optimization")

    st.markdown(
        """
Configure the optimization algorithm and run the logistics optimization.
"""
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        population = st.slider(
            "Population Size",
            10,
            100,
            30,
            5
        )

        generations = st.slider(
            "Generations",
            20,
            500,
            100,
            10
        )

    with col2:

        mutation = st.slider(
            "Mutation Rate",
            0.01,
            0.50,
            0.10,
            0.01
        )

        cooling = st.slider(
            "Cooling Rate",
            0.80,
            0.99,
            0.95,
            0.01
        )

    st.divider()

    if st.button(
        "🚀 Run Optimization",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner("Running Genetic Algorithm..."):

            service = OptimizationService()

            result = service.optimize(
                population_size=population,
                generations=generations,
                mutation_rate=mutation,
                cooling_rate=cooling,
            )

        st.session_state["optimization_result"] = result

        st.success("Optimization Completed!")

        st.rerun()

    if "optimization_result" in st.session_state:

        result = st.session_state["optimization_result"]

        st.divider()

        st.subheader("Fitness History")

        fitness_df = pd.DataFrame(
            {
                "Generation": range(
                    1,
                    len(result.fitness_history) + 1
                ),
                "Fitness": result.fitness_history
            }
        )

        st.line_chart(
            fitness_df.set_index("Generation")
        )

        st.success(
            "Optimization result has been saved.\n\nGo to the Dashboard page to view the complete report."
        )