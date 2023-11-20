from django import forms
from .models import Category, Post, Comment

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,  # Hace que el campo sea obligatorio
        label='Categoría'
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'image': 'Imagen',
        }

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['content', 'parent_id']