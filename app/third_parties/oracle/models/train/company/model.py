from sqlalchemy import VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import CustomBaseModel, Base


class Company(Base, CustomBaseModel):
    __tablename__ = 'company'

    name = Column(VARCHAR(105), nullable=False, comment='Tên công ty')
    address = Column(VARCHAR(100), comment='Địa chỉ công ty')
