from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.User)
admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.TeacherUser)
admin.site.register(models.WordAdmin)
