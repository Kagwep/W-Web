from django.contrib import admin

from .models import UserReg,Mystory,Comment,Topic

# Register your models here.
admin.site.register(UserReg)
admin.site.register(Mystory)
admin.site.register(Comment)
admin.site.register(Topic)