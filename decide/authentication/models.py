from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as trans

# Create your models here.

def validate_postal_code(value):
    if value > 99999 or value < 11111:
        raise ValidationError(
            trans('%(value)s is not a valid postal code'),
            params={'value': value},
        )

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    postal_code = models.IntegerField(validators=[validate_postal_code])
