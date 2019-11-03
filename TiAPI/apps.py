from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class TiapiConfig(AppConfig):
    name = 'TiAPI'


class TiapiAdminConfig(AdminConfig):
    default_site = "TiAPI.admin.MyAdmin"
