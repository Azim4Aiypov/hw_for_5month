from datetime import date
from rest_framework.exceptions import ValidationError

def validate_age(birthdate):
    if birthdate is None:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")
