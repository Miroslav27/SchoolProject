"""
1. Написати АПІ для Груп, Студентів та Вчителів (CRUD)
2.Доступ до АПІ має бути лише у аутинтифікованих користувачів
3.Підключити Аутинтификацию через Токен
4. Генерувати новий токен що півночі
"""


from rest_framework import serializers

class StudentSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    firstname = serializers.CharField()
    surname = serializers.CharField()

