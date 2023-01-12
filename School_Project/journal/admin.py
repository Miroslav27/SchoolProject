from django.contrib import admin
from journal import models
# Register your models here.
admin.site.register(models.Group)
admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.Course)
admin.site.register(models.CourseCategory)
admin.site.register(models.Tag)
admin.site.register(models.Currency)
