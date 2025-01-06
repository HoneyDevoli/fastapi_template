from app.entity.base.pageable import PageRequestSchema
from app.entity.order.db import OrderOrm
from app.entity.order.repository import OrderRepository


class OrderService:
    def __init__(self):
        self.order_repo: OrderRepository = OrderRepository()

    def create_order(self, order: OrderOrm) -> OrderOrm:
        return self.order_repo.save(order)

    def get_order(self, order_id: int) -> OrderOrm:
        return self.order_repo.get_by_id(order_id)

    def get_order_by_address_id(self, address_id: int) -> OrderOrm:
        return self.order_repo.get_by_address_id(address_id)

    def update_order(self, order_id: int, updated_order: OrderOrm):
        order: OrderOrm = self.order_repo.get_by_id(order_id)
        order.name = updated_order.name
        order.price = updated_order.price
        return self.order_repo.save(order)

    def get_paged_orders(self, pageable: PageRequestSchema) -> tuple[list, int]:
        return self.order_repo.get_paged_items(pageable, {})
