from sqlalchemy import text

from database.connection import get_session
from models.goods import Goods


class GoodsRepository:

    def get_all_goods(self):
        """
        Returns all pending goods as Goods objects.
        """

        session = get_session()

        try:

            query = text("""
                SELECT
                    item_id,
                    item_name,
                    destination_city,
                    weight_kg,
                    volume_m3,
                    dimension_type,
                    days_waiting,
                    status
                FROM daily_goods_queue
                WHERE status = 'Pending'
                ORDER BY item_id
            """)

            result = session.execute(query)

            goods = []

            for row in result.mappings():

                goods.append(
                    Goods(
                        item_id=row["item_id"],
                        item_name=row["item_name"],
                        destination_city=row["destination_city"],
                        weight_kg=float(row["weight_kg"]),
                        volume_m3=float(row["volume_m3"]),
                        dimension_type=row["dimension_type"],
                        days_waiting=row["days_waiting"],
                        status=row["status"]
                    )
                )

            return goods

        finally:
            session.close()

    def update_status(self, item_id, status):

        session = get_session()

        try:

            query = text("""
                UPDATE daily_goods_queue
                SET status = :status
                WHERE item_id = :item_id
            """)

            session.execute(
                query,
                {
                    "item_id": item_id,
                    "status": status
                }
            )

            session.commit()

        finally:
            session.close()

    def add_goods(
        self,
        item_id,
        item_name,
        destination_city,
        weight_kg,
        volume_m3,
        dimension_type,
        days_waiting,
    ):

        session = get_session()

        try:

            query = text("""
                INSERT INTO daily_goods_queue
                (
                    item_id,
                    item_name,
                    destination_city,
                    weight_kg,
                    volume_m3,
                    dimension_type,
                    days_waiting,
                    status
                )
                VALUES
                (
                    :item_id,
                    :item_name,
                    :destination_city,
                    :weight_kg,
                    :volume_m3,
                    :dimension_type,
                    :days_waiting,
                    'Pending'
                )
            """)

            session.execute(
                query,
                {
                    "item_id": item_id,
                    "item_name": item_name,
                    "destination_city": destination_city,
                    "weight_kg": weight_kg,
                    "volume_m3": volume_m3,
                    "dimension_type": dimension_type,
                    "days_waiting": days_waiting,
                },
            )

            session.commit()

        finally:
            session.close()

    def delete_goods(self, item_id):

        session = get_session()

        try:

            query = text("""
                DELETE
                FROM daily_goods_queue
                WHERE item_id = :item_id
            """)

            session.execute(
                query,
                {
                    "item_id": item_id
                }
            )

            session.commit()

        finally:
            session.close()

    def update_goods(
        self,
        item_id,
        item_name,
        destination_city,
        weight_kg,
        volume_m3,
        dimension_type,
        days_waiting,
    ):

        session = get_session()

        try:

            query = text("""
                UPDATE daily_goods_queue
                SET
                    item_name = :item_name,
                    destination_city = :destination_city,
                    weight_kg = :weight_kg,
                    volume_m3 = :volume_m3,
                    dimension_type = :dimension_type,
                    days_waiting = :days_waiting
                WHERE
                    item_id = :item_id
            """)

            session.execute(
                query,
                {
                    "item_id": item_id,
                    "item_name": item_name,
                    "destination_city": destination_city,
                    "weight_kg": weight_kg,
                    "volume_m3": volume_m3,
                    "dimension_type": dimension_type,
                    "days_waiting": days_waiting,
                },
            )

            session.commit()

        finally:
            session.close()

    def get_goods_by_id(self, item_id):

        session = get_session()

        try:

            query = text("""
                SELECT *
                FROM daily_goods_queue
                WHERE item_id = :item_id
            """)

            result = session.execute(
                query,
                {
                    "item_id": item_id
                }
            ).mappings().first()

            if result is None:
                return None

            return Goods(
                item_id=result["item_id"],
                item_name=result["item_name"],
                destination_city=result["destination_city"],
                weight_kg=float(result["weight_kg"]),
                volume_m3=float(result["volume_m3"]),
                dimension_type=result["dimension_type"],
                days_waiting=result["days_waiting"],
                status=result["status"],
            )

        finally:
            session.close()