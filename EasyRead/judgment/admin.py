from django.contrib import admin
from .models import User, UserRating, UserComment

admin.site.register(User)
admin.site.register(UserRating)
admin.site.register(UserComment)