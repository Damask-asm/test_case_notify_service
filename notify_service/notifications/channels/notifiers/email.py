from notify_service.notifications.channels.base import BaseNotifier
from notify_service.notifications.channels.exceptions import ChannelUnavailableError


class EmailNotifier(BaseNotifier):
    def send(self, user, message):
        if not user.email:
            raise ChannelUnavailableError("У пользователя нет email")
        print(f"[EMAIL] {user.email}: {message}")
