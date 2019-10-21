from datetime import datetime

from django.db import models
from django.utils.timezone import now


class UserModel(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    surname = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)


class CodeModel(models.Model):
    code_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=False, null=False)
    created = models.DateTimeField(default=now)
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
