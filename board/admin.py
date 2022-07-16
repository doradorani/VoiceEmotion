from django.contrib import admin

from .models import Board, Notice, Comment

admin.site.register(Notice)
admin.site.register(Board)
admin.site.register(Comment)
