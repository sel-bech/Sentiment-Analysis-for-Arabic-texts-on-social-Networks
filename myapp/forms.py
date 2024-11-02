from django.forms import ModelForm, TextInput, Textarea
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)