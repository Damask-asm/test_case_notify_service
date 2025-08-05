
# 📬 Notify Service

**Notify Service** — микросервис уведомлений на Django, поддерживающий многоканальную отправку сообщений (Email, SMS, Telegram и др.) через расширяемую систему нотификаторов.

---

## 📦 Особенности

- ✅ Модульная архитектура с авто-регистрацией каналов
- 📧 Поддержка отправки через Email, SMS, Telegram
- ⚙️ Простая интеграция с другими микросервисами
- 🔐 Проверка доступа по API-ключу (permissions)
- 📚 Автоматическая генерация OpenAPI схем через drf-spectacular

---

## 🛠️ Стек технологий

- Python 3.12+
- Django 5.x
- Django REST Framework
- drf-spectacular
- Celery (опционально)
- Redis (опционально)

---

## 🚀 Быстрый старт

### 1. Клонируй репозиторий:

```bash
git clone https://github.com/Damask-asm/test_case_notify_service.git
cd notify_service
```

### 2. Установи зависимости:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Создай `.env` файл:

```ini
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=secret
REDIS_URL=redis://localhost:6379/0
```

### 4. Примени миграции и запусти сервер:

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🧱 Архитектура

```
notify_service/
├── manage.py
├── notify_service/              # Django settings, urls
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── notifications/               # Основное приложение
│   ├── models.py
│   ├── views.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── channels/
│   │   ├── base.py
│   │   ├── registry.py
│   │   └── notifiers/
│   │       ├── email.py
│   │       ├── sms.py
│   │       ├── telegram.py
│   │       └── ...
│   └── ...
```

---

## 📤 Добавление нового канала

Создай файл в `notifications/channels/notifiers/`, например `whatsapp.py`:

```python
from notifications.channels.base import BaseNotifier

class WhatsAppNotifier(BaseNotifier):
    def send(self, message: str, user: UserNotification):
        # реализуй отправку через WhatsApp API
        ...
```

Регистрироваться будет автоматически при запуске.

---

## 📘 Документация API

После запуска:

- Swagger: [`/api/schema/swagger/`](http://localhost:8000/api/schema/swagger/)
- ReDoc: [`/api/schema/redoc/`](http://localhost:8000/api/schema/redoc/)

---

## 🧪 Тестирование

```bash
python manage.py test
```

---

## 📄 Лицензия

MIT License © 2025 Храмов Андрей Витальевич

---

## 🧠 Автор

Разработка и архитектура: [Андрей Храмов](mailto:andrey@example.com)
```