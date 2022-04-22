from django.contrib import admin

from .models import Board, Notice

admin.site.register(Notice)
admin.site.register(Board)
