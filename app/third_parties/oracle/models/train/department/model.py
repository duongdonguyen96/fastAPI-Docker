from sqlalchemy import VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import CustomBaseModel, Base
from app.third_parties.oracle.models.train.company.model import Company


class Department(Base, CustomBaseModel):
    __tablename__ = 'department'

    name = Column(VARCHAR(105), nullable=False, comment='Tên phòng ban')

    company_id = Column(ForeignKey('company.id'), nullable=True)

    company = relationship('Company')
