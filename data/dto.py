import uuid

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

from .models import DeviceStatus, DeviceType


class DeviceDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: DeviceType
    name: str = "new device"
    description: Optional[str] = None
    status: DeviceStatus

    class Config:
        from_attributes = True


class ConnectionDTO(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    device_a: str
    device_b: str

    class Config:
        from_attributes = True