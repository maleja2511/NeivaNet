# context_processors.py en tu aplicación (por ejemplo, en la carpeta posts)
from django.db.models import Avg
from django.db.models.functions import Coalesce
from .models import Category, Post
from .views import Round

def categories_ranking(request):
    categories_with_ranking = Category.objects.all().annotate(
        average_score=Coalesce(Round(Avg('post__ranking')), 0)
    ).order_by('-average_score')
    
    return {'categories_with_ranking': categories_with_ranking}