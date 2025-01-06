import logging

from sqlalchemy import or_
from sqlalchemy.exc import NoResultFound

from app.entity.base.repository import BaseRepository
from app.entity.order.db import OrderOrm
from app.utils.db import get_db

logger = logging.getLogger(__name__)


class OrderRepository(BaseRepository):
    def __init__(self):
        super().__init__(OrderOrm)

    def get_by_address_id(self, address_id: int):
        with get_db() as db:
            try:
                clause = or_(OrderOrm.pickup_id == address_id, OrderOrm.dropoff_id == address_id)
                return db.query(self.__model__).filter(clause).one()
            except NoResultFound as e:
                logger.exception(f'{self.__model__.__name__} not found with address id: {id}')
                raise e
