from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'image': 'Imagen',
            'category': 'Categoría',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']