from django import forms

from .models import Post, User, Comment


class PostForm(forms.ModelForm):
    """Форма поста."""

    class Meta:
        model = Post
        exclude = ('author', 'is_published',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class UserForm(forms.ModelForm):
    """Форма юзера."""

    class Meta:
        model = User
        fields = '__all__'


class CommentForm(forms.ModelForm):
    """Форма комментариев."""

    class Meta:
        model = Comment
        fields = ('text',)
