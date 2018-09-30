from django.contrib import admin
from .models import Post, DocPost, AdminPost
admin.site.register(Post,  AdminPost)
# Register your models here.
