from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from app.entity.base.pageable import PageRequestSchema, PageResponseSchema
from app.entity.order.service import OrderService
from app.entity.order.v1.schema import OrderIn, OrderOut

router = APIRouter(prefix='/api/v1', tags=['Order'])


@router.post('/order', status_code=HTTP_201_CREATED, operation_id='create_order', response_model=OrderOut)
def create_order(order: OrderIn, order_service: OrderService = Depends(OrderService)) -> OrderOut:
    return OrderOut.model_validate(order_service.create_order(order.to_orm()))


@router.get('/order/{order_id}', operation_id='get_order', response_model=OrderOut)
def get_order(order_id: int, order_service: OrderService = Depends(OrderService)) -> OrderOut:
    return OrderOut.model_validate(order_service.get_order(order_id))


@router.get('/order/address/{address_id}', operation_id='get_order_by_address', response_model=OrderOut)
def get_order_by_address(address_id: int, order_service: OrderService = Depends(OrderService)) -> OrderOut:
    return OrderOut.model_validate(order_service.get_order_by_address_id(address_id))


@router.put('/order/{order_id}', operation_id='update_order', response_model=OrderOut)
def update_order(order_id: int, order: OrderIn, order_service: OrderService = Depends(OrderService)) -> OrderOut:
    return OrderOut.model_validate(order_service.update_order(order_id, order))


@router.get('/order', operation_id='list_orders', response_model=PageResponseSchema)
def list_orders(
    pageable: PageRequestSchema = Depends(), order_service: OrderService = Depends(OrderService)
) -> PageResponseSchema:
    data, total_count = order_service.get_paged_orders(pageable)
    response = PageResponseSchema(
        total_count=total_count, page_size=pageable.size, data=[OrderOut.model_validate(orm) for orm in data]
    )
    return response
