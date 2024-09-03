from django.contrib import admin
from .models import Post, Reply

# Register your models here.
admin.site.register((Post, Reply))