from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def send_course_update_notification(course_id):
    """
    Асинхронная задача для отправки уведомлений об обновлении курса
    """
    from materials.models import Rate
    from user.models import Subscription

    try:
        course = Rate.objects.get(id=course_id)

        # Проверяем, что курс не обновлялся более 4 часов
        four_hours_ago = datetime.now() - timedelta(hours=4)
        if course.updated_at > four_hours_ago:
            # Если курс обновлялся менее 4 часов назад, не отправляем уведомления
            return f"Курс {course.name} обновлялся менее 4 часов назад. Уведомления не отправлены."

        # Получаем всех подписчиков курса
        subscriptions = Subscription.objects.filter(
            course=course, user__is_active=True
        ).select_related("user")

        if not subscriptions:
            return f"Нет активных подписчиков для курса {course.name}"

        # Формируем сообщение
        subject = f"Обновление курса: {course.name}"
        message = f"""
        Здравствуйте!
        Курс "{course.name}" был обновлен.
        Описание курса: {course.description or 'Описание не указано'}
        Переходите на платформу, чтобы ознакомиться с обновлениями!
        С уважением,
        Команда образовательной платформы
        """

        # Отправляем письма всем подписчикам
        sent_count = 0
        for subscription in subscriptions:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscription.user.email],
                    fail_silently=False,
                )
                sent_count += 1
            except Exception as e:
                print(
                    f"Ошибка отправки письма пользователю {subscription.user.email}: {e}"
                )

        return f"Отправлено {sent_count} уведомлений для курса {course.name}"

    except Rate.DoesNotExist:
        return f"Курс с ID {course_id} не найден"
    except Exception as e:
        return f"Ошибка при отправке уведомлений: {e}"
