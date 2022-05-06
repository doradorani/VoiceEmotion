from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from member.models import User
# Create your models here.

User = get_user_model()


class Board(models.Model):
    RESPONSE_CHOICES = (('no', 'No'), ('yes', 'Yes'))

    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    content = models.TextField(null=False)
    image = models.FileField(null=True, blank=True, upload_to='img/%y/%m/%d')
    date = models.DateTimeField(default=now, editable=False, null=False)
    response = models.CharField(default='no', max_length=5, choices=RESPONSE_CHOICES)

    class Meta:
        db_table = 'board'


class Comment(models.Model):
    username = models.CharField(default='익명의 니모션',max_length=10,null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now, editable=False, null=False)
    content = models.TextField()

    class Meta:
        db_table = 'comment'


class Notice(models.Model):
    title = models.CharField(max_length=45)
    content = models.CharField(max_length=400)
    date = models.DateTimeField(default=now, editable=False, null=False)
    username = models.CharField(max_length=45, default='관리자')

    class Meta:
        db_table = 'notice'
