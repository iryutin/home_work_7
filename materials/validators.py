from django.core.exceptions import ValidationError

def youtubefiltr (video):
    if 'youtube.com' not in video.lower() and 'youtu.be' not in video.lower():
        raise ValidationError(
            f"Ссылки на сторонние ресурсы запрещены. Обнаружена ссылка: {video}"
        )