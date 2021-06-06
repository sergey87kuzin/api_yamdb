import datetime

from django.utils.translation import ugettext as _

from rest_framework.serializers import ValidationError


def validator_year(value):
    if -5500 > value > datetime.date.today().year + 50:
        raise ValidationError(
            _('Несуществующий год',
              code='invalid',
              params={'value': value})
        )
