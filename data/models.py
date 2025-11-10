from sqlalchemy import Column, String, Integer, Float, JSON, Enum, Text, TIMESTAMP, ForeignKey
import enum
import uuid

from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class DeviceStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class ConnectionStatus(enum.Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class DeviceType(enum.Enum):
    PC = "PC"
    NETWORK_DEVICE = "network_device"


class Device(Base):
    __tablename__ = 'devices'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(Enum(DeviceType))
    name = Column(String)
    description = Column(Text)
    status = Column(Enum(DeviceStatus))


class Connection(Base):
    __tablename__ = 'connections'

    id = Column(String, primary_key=True)
    device_a = Column(String, ForeignKey("devices.id"), nullable=False)
    device_b = Column(String, ForeignKey("devices.id"), nullable=False)
    status = Column(Enum(DeviceStatus))


class ConnectionHistory(Base):
    __tablename__ = 'connection_history_records'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    connection = Column(String, ForeignKey("connections.id"), nullable=False)
    change_date = Column(TIMESTAMP)
    status = Column(Enum(ConnectionStatus))
    description = Column(Text)

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
