from rest_framework.response import Response
from rest_framework import status as drf_status


class CustomResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        success = 200 <= response.status_code < 300

        # Получаем язык пользователя
        lang = 'uz'
        if hasattr(request, 'user') and request.user.is_authenticated:
            lang = getattr(request.user, 'language', 'uz')

        # Переводы сообщений
        status_messages = {
            'uz': {
                200: "muvaffaqiyatli",
                201: "yaratildi",
                204: "oʻchirildi",
                400: "tasdiqlashda xatolik",
                401: "avtorizatsiya qilinmagan",
                403: "taqiqlangan",
                404: "topilmadi",
                405: "metodga ruxsat yoʻq",
                500: "server xatosi",
            },
            'ru': {
                200: "успешно",
                201: "создано",
                204: "удалено",
                400: "ошибка валидации",
                401: "неавторизован",
                403: "доступ запрещён",
                404: "не найдено",
                405: "метод не разрешён",
                500: "внутренняя ошибка сервера",
            },
            'en': {
                200: "success",
                201: "created",
                204: "deleted",
                400: "validation error",
                401: "unauthorized",
                403: "forbidden",
                404: "not found",
                405: "method not allowed",
                500: "internal server error",
            }
        }

        # Получаем message по статусу и языку
        message = status_messages.get(lang, status_messages['uz']).get(
            response.status_code,
            "xatolik" if not success else "muvaffaqiyatli"
        )

        # Формируем итоговый ответ
        response_data = {
            'status': success,
            'message': message if success else response.data,
            'data': response.data if success else [],
        }

        response.data = response_data
        response._is_rendered = False  # сбрасываем отрендеренный ответ

        return super().finalize_response(request, response, *args, **kwargs)