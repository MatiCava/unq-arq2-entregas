from fastapi import APIRouter, Response
from application.notifications_service import notifications_service
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from domain.notifications import Notification

notifications_router = APIRouter()

@notifications_router.post('/notifications', response_model=Notification, tags=["Notifications"])
def send_notification(notification: Notification):
    result = notifications_service.send_notification(notification)
    if result["error_msg"]:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    return Response(status_code=HTTP_200_OK)
