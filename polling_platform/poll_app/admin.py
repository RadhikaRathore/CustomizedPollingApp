from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from poll_app.models import User, Poll, EmailId, Choice
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Poll)
admin.site.register(EmailId)
admin.site.register(Choice)
