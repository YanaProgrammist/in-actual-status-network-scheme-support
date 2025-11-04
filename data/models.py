# from sqlalchemy import Column, String, Integer, Float, JSON, Enum, Text, TIMESTAMP
# from sqlalchemy.ext.declarative import declarative_base
import enum
# import uuid
#
# from sqlalchemy.orm import relationship
#
# Base = declarative_base()
#
#
class DeviceStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class DeviceType(enum.Enum):
    PC = "PC"
    NETWORK_DEVICE = "network_device"

#
# class Device(Base):
#     __tablename__ = 'devices'
#
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     type = Column(Enum(DeviceType))
#     name = Column(String)
#     description = Column(Text)
#     status = Column(Enum(DeviceStatus))
#     location = relationship("Location", back_populates="devices")
#     # Координаты для отображения на схеме
#     x = Column(Float)
#     y = Column(Float)
#
#
# class Location(Base):
#     __tablename__ = 'locations'
#
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = Column(String)
#     devices = relationship("Device", back_populates="location")
#     connections = relationship("Connection", back_populates="location")
#     connection_history_records = relationship("ConnectionHistory", back_populates="location")
#
#
# class Connection(Base):
#     __tablename__ = 'connections'
#
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     location = relationship("Location", back_populates="connections")
#     device_a = Column(Integer, ForeignKey("devices.id"), nullable=False)
#     device_b = Column(Integer, ForeignKey("devices.id"), nullable=False)
#
#
# class ConnectionHistory(Base):
#     __tablename__ = 'connection_history_records'
#
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     location = relationship("Location", back_populates="connection_history_records")
#     device_a = Column(Integer, ForeignKey("devices.id"), nullable=False)
#     device_b = Column(Integer, ForeignKey("devices.id"), nullable=False)
#     change_date = Column(TIMESTAMP)
#     description = Column(Text)
