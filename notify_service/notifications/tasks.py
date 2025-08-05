import logging

from celery import shared_task
from django.utils import timezone

from .channels import CHANNEL_MAP
from .models import UserNotification, NotificationLog
from .channels.exceptions import ChannelUnavailableError

logger = logging.getLogger("notify_service.notifications")

@shared_task
def send_notification_task(user_id, message, channels):
    user = UserNotification.objects.get(id=user_id)

    for channel in channels:
        notifier = CHANNEL_MAP.get(channel)
        if not notifier:
            continue

        log = NotificationLog.objects.create(
            user=user,
            channel=channel,
            message=message,
            status='pending'
        )

        try:
            notifier.send(user, message)
            log.status = 'success'
            log.sent_at = timezone.now()
            log.save()
            logger.info(f"[SUCCESS] {channel.upper()} для пользователя ID={user.id}")
            break
        except ChannelUnavailableError as e:
            log.status = 'unavailable'
            log.sent_at = timezone.now()
            log.error_message = str(e)
            log.save()
            logger.info(f"[UNAVAILABLE] {channel.upper()} для пользователя ID={user.id}")
            continue
        except Exception as e:
            log.status = 'failed'
            log.sent_at = timezone.now()
            log.error_message = str(e)
            logger.warning(f"[FAILED] {channel.upper()} для пользователя ID={user.id}")
            log.save()
            continue
