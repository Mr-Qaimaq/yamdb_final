from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(year):
    if not (0 < year < dt.now().year):
        raise ValidationError('Указан неверный год')
