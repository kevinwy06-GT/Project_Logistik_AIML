import streamlit as st
import pandas as pd

from database.truck_repository import TruckRepository

repo = TruckRepository()


def show():

    st.title("🚚 Truck Management")

    trucks = repo.get_all_trucks()

    if len(trucks) == 0:

        st.warning("No trucks found.")

        return

    # ===========================================
    # Truck Table
    # ===========================================

    rows = []

    for truck in trucks:

        rows.append(
            {
                "Truck ID": truck.truck_id,
                "License Plate": truck.license_plate,
                "Max Weight (kg)": truck.max_weight_kg,
                "Max Volume (m³)": truck.max_volume_m3,
                "Fuel Cost/km": truck.fuel_cost_per_km,
                "Maintenance/km": truck.maint_cost_per_km,
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ===========================================
    # Edit Truck
    # ===========================================

    st.subheader("✏ Edit Truck")

    selected = st.selectbox(
        "Select Truck",
        [truck.truck_id for truck in trucks],
    )

    truck = repo.get_truck_by_id(selected)

    with st.form("truck_form"):

        max_weight = st.number_input(
            "Maximum Weight (kg)",
            value=float(truck.max_weight_kg),
        )

        max_volume = st.number_input(
            "Maximum Volume (m³)",
            value=float(truck.max_volume_m3),
        )

        fuel_cost = st.number_input(
            "Fuel Cost per km",
            value=float(truck.fuel_cost_per_km),
        )

        maintenance_cost = st.number_input(
            "Maintenance Cost per km",
            value=float(truck.maint_cost_per_km),
        )

        submitted = st.form_submit_button(
            "💾 Save Changes",
            use_container_width=True,
        )

        if submitted:

            repo.update_truck(
                truck.truck_id,
                max_weight,
                max_volume,
                fuel_cost,
                maintenance_cost,
            )

            st.success("Truck updated successfully!")

            st.rerun()