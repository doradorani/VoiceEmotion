from django import forms
from .models import Board, Comment

class BoardWriteForm(forms.ModelForm):
    
    class Meta:
        model = Board
        fields = ('title','content', 'image',)




class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        labels = {
        'content': '댓글내용',
        }