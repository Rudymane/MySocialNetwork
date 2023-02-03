from django.contrib import admin
from .models import Posts, User, Following
# Register your models here.

admin.site.register(Posts)
admin.site.register(User)
admin.site.register(Following)