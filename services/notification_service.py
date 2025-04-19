# service/notification_service.py
from patterns.observer import NotificationService

notify = NotificationService.get_instance().send
