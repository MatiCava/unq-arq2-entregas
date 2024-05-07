from pydantic import BaseModel
from adapters.notifications_adapter import notifications_adapter

class Notification(BaseModel):
    email_seller: list[str]
    email_user: str

    def send_notification(notification: 'Notification') -> None:
        notifications_adapter.send_notification(Notification.parse_notification(notification))

    def parse_notification(notification: 'Notification') -> dict:
        new_notification = dict(notification)
        return new_notification