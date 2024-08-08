from django.contrib import admin
from .models import User, UserRating, LowPoint

admin.site.register(User)
admin.site.register(UserRating)
admin.site.register(LowPoint)