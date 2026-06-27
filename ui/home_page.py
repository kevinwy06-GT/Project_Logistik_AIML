import streamlit as st


def show():

    st.title("🚚 Logistics Optimization System")

    st.markdown(
        """
Welcome to the **AI Logistics Optimization System**.

This application optimizes daily truck loading using:

- 🧬 Genetic Algorithm
- 🔥 Simulated Annealing

Developed for the Artificial Intelligence & Machine Learning course.
"""
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Algorithms",
        "2"
    )

    col2.metric(
        "Fleet",
        "4 Trucks"
    )

    col3.metric(
        "Database",
        "MySQL"
    )

    st.info(
        "Use the sidebar to navigate through the application."
    )