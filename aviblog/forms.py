from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    """Post Share Form"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.CharField(max_length=25)
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        