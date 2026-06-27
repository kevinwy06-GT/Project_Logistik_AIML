import streamlit as st
import pandas as pd

from database.goods_repository import GoodsRepository

repo = GoodsRepository()


def show():

    st.title("📦 Goods Management")

    # =====================================================
    # ADD NEW GOODS
    # =====================================================

    with st.expander("➕ Add New Goods", expanded=False):

        with st.form("add_goods_form"):

            item_id = st.text_input("Item ID")

            item_name = st.text_input("Item Name")

            destination = st.selectbox(
                "Destination City",
                [
                    "Malang",
                    "Kediri",
                    "Madiun",
                    "Jember",
                    "Banyuwangi",
                    "Probolinggo",
                    "Tuban",
                    "Blitar",
                    "Pasuruan",
                    "Mojokerto",
                    "Batu"
                ]
            )

            col1, col2 = st.columns(2)

            with col1:
                weight = st.number_input(
                    "Weight (kg)",
                    min_value=1.0,
                    step=1.0
                )

                volume = st.number_input(
                    "Volume (m³)",
                    min_value=0.1,
                    step=0.1
                )

            with col2:

                dimension = st.selectbox(
                    "Dimension",
                    ["S", "M", "L"]
                )

                waiting = st.number_input(
                    "Days Waiting",
                    min_value=0,
                    step=1
                )

            submitted = st.form_submit_button(
                "Add Goods",
                use_container_width=True
            )

            if submitted:

                if item_id == "" or item_name == "":

                    st.error(
                        "Item ID and Item Name are required."
                    )

                else:

                    repo.add_goods(
                        item_id,
                        item_name,
                        destination,
                        weight,
                        volume,
                        dimension,
                        waiting
                    )

                    st.success("Goods added successfully!")

                    st.rerun()

    st.divider()

    # =====================================================
    # GOODS TABLE
    # =====================================================

    goods = repo.get_all_goods()

    if len(goods) == 0:

        st.warning("No goods available.")

        return

    table = []

    for item in goods:

        table.append(
            {
                "ID": item.item_id,
                "Name": item.item_name,
                "Destination": item.destination_city,
                "Weight": item.weight_kg,
                "Volume": item.volume_m3,
                "Dimension": item.dimension_type,
                "Waiting": item.days_waiting,
                "Status": item.status
            }
        )

    st.dataframe(
        pd.DataFrame(table),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================================
    # DELETE GOODS
    # =====================================================

    st.subheader("🗑 Delete Goods")

    ids = [g.item_id for g in goods]

    selected = st.selectbox(
        "Select Item",
        ids
    )

    if st.button(
        "Delete Selected Item",
        type="primary"
    ):

        repo.delete_goods(selected)

        st.success("Item deleted.")

        st.rerun()