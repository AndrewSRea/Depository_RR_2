from django.contrib import admin
from .models import Album, Review, User


admin.site.register(User)
admin.site.register(Album)
admin.site.register(Review)