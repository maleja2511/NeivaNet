from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    RANKING_CHOICES = [(x / 2, str(x / 2)) for x in range(0, 11)]

    ranking = forms.TypedChoiceField(
        choices=RANKING_CHOICES, 
        coerce=float,
        empty_value=None,
        widget=forms.Select(),
        label='Ranking'
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'ranking']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']