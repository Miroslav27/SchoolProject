from django.contrib import admin
from journal import models
# Register your models here.
admin.site.register(models.Group)
admin.site.register(models.Teacher)
admin.site.register(models.Student)