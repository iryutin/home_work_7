from django.core.exceptions import ValidationError


class YoutubeFiltrValidator:
    def __call__(self, video):
        if "youtube.com" not in video.lower() and "youtu.be" not in video.lower():
            raise ValidationError(
                f"Ссылки на сторонние ресурсы запрещены. Обнаружена ссылка: {video}"
            )

    @classmethod
    def __fields__(cls):
        return ["video"]
