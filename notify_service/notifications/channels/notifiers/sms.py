from notify_service.notifications.channels.base import BaseNotifier
from notify_service.notifications.channels.exceptions import ChannelUnavailableError


class SmsNotifier(BaseNotifier):
    def send(self, user, message):
        if not user.phone:
            raise ChannelUnavailableError("У пользователя нет номера телефона")
        print(f"[SMS] {user.phone}: {message}")
