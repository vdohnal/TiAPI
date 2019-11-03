from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import models

import TiAPI.models as my_models


class MyAdmin(AdminSite):
    site_header = "TiAPI admin page"
    site_title = "TiAPI admin"


admin.site = MyAdmin()
admin.site.register(models.User)
admin.site.register(models.Group)
admin.site.register(models.Permission)
admin.site.register(my_models.CodeModel)
admin.site.register(my_models.CodeGroupModel)
admin.site.register(my_models.UserModel)
