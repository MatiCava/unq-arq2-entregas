from typing import Any
from domain.notifications import Notification
import re

class notifications_service:
    
    def send_notification(notification: Notification) -> dict:
        error = {"error_msg": ''}
        check_seller = True
        check_user = notifications_service.validate_email(notification.email_user)
        for email_seller in notification.email_seller:
            check_seller = check_seller and notifications_service.validate_email(email_seller)
        if check_seller and check_user:
            Notification.send_notification(notification)
        else:
            error["error_msg"] = 'One of the emails is invalid!'
        return error
    
    def validate_email(email: str) -> bool:
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) and ' ' not in email