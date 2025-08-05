from abc import ABC, abstractmethod


class BaseNotifier(ABC):
    @abstractmethod
    def send(self, user: "UserNotification", message: str):
        """Отправить уведомление пользователю."""
        pass
