from data.database import db
from data.dto import DeviceDTO
from data.models import Device


def get_all_devices():
    with db.get_session() as session:
        return [DeviceDTO.model_validate(device) for device in session.query(Device).all()]


def add_device(device: Device):
    with db.get_session() as session:
        session.add(device)
        return device


def update_device(device: DeviceDTO):
    with db.get_session() as session:
        session.query(Device) \
            .filter(Device.id == device.id) \
            .update(device.model_dump())
        return device


def delete_device(device_id: str):
    with db.get_session() as session:
        device = session.query(Device).filter_by(id=device_id).first()
        if device:
            session.delete(device)
