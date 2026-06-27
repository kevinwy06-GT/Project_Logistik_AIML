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