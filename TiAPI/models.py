from django.db import models
from django.utils.timezone import now


class UserModel(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    surname = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username


class CodeGroupModel(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class CodeModel(models.Model):
    code = models.CharField(max_length=50, blank=False, null=False, primary_key=True)
    created = models.DateTimeField(default=now)
    last_used = models.DateTimeField(default=None)
    group = models.ForeignKey(CodeGroupModel, on_delete=models.DO_NOTHING, blank=False, null=False)
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.code
