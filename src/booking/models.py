from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from boats.models import Boat


class Booking(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered      = models.BooleanField(default=False)
    boat         = models.ForeignKey(Boat, on_delete=models.CASCADE)
    invited_date = models.DateTimeField()
    return_date  = models.DateTimeField()
    price        = models.DecimalField(decimal_places=2, max_digits=20, default=100.00)
