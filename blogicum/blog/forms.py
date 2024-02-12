from django import forms
from .models import Post, Comment, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
