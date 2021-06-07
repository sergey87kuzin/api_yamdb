import datetime
from rest_framework.serializers import ValidationError


def validator_year(value):
    if -5500 > value > datetime.date.today().year + 50:
        raise ValidationError(
            'Несуществующий год',
            code='invalid',
            params={'value': value}
        )
