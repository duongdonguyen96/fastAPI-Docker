# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import VARCHAR, Column, DateTime, text
# from sqlalchemy.dialects.oracle import NUMBER
# from app.settings.database import DB_CONFIG
#
# DATABASE_URL = "mysql+mysqlconnector://{user_name}:{password}@{host}:{port}/{service_name}".format_map({
#     'host': DB_CONFIG['host'],
#     'port': DB_CONFIG['port'],
#     'user_name': DB_CONFIG['user_name'],
#     'password': DB_CONFIG['password'],
#     'service_name': DB_CONFIG['service_name']
# })
#
# engine = create_engine(DATABASE_URL)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
# metadata = Base.metadata
#
#
# class CustomBaseModel:
#     id = Column(VARCHAR(32), primary_key=True, server_default=text("sys_guid()"), comment='Mã gen tự động')
#     update_by = Column(VARCHAR(32), server_default=text("sys_guid()"))
#     create_by = Column(VARCHAR(32), server_default=text("sys_guid()"))
#     date_create = Column(DateTime, comment='ngày tạo')
#     date_update = Column(DateTime, comment='ngày cập nhật cuối cùng')
#     is_delete = Column(NUMBER(1, 0, False), comment='trạng thái hoạt động')