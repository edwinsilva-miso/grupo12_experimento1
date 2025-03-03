import enum
import uuid
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database.declarative_base import Base


class StatusEnum(enum.Enum):
    POR_VERIFICAR = 'POR_VERIFICAR'
    NO_VERIFICADO = 'NO_VERIFICADO'
    VERIFICADO = 'VERIFICADO'


class ProductModel(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String)
    # description = Column(String)
    price = Column(Float)
    # stock = Column(Integer)
    # status = Column(sqlalchemy.Enum(StatusEnum), default=StatusEnum.POR_VERIFICAR)
    # expireAt = Column(DateTime, nullable=True)
    # createdAt = Column(DateTime, nullable=True, default=datetime.utcnow)
    # updatedAt = Column(DateTime, nullable=True)
