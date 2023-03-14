from sqlalchemy import VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import CustomBaseModel, Base

from app.third_parties.oracle.models.train.company.model import Company
from app.third_parties.oracle.models.train.department.model import Department


class Customer(Base, CustomBaseModel):
    __tablename__ = 'customer'

    full_name = Column(VARCHAR(105), nullable=False, comment='Tên đầy đủ')
    email = Column(VARCHAR(100), comment='Email')
    phone = Column(VARCHAR(12), comment='Số điện thoại')
    user_name = Column(VARCHAR(50), comment='tên tài khoản', unique=True)
    password = Column('password', VARCHAR(50), comment='Mật khẩu')

    company_id = Column(ForeignKey('company.id'), nullable=True)
    department_id = Column(ForeignKey('department.id'), nullable=True)

    department = relationship('Department')
    company = relationship('Company')
