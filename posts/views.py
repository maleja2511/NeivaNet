from django.shortcuts import redirect, render
from django.db import models
from posts.models import Post, Like
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import Category, Comment
from django.db.models import Func, IntegerField
from django.db.models.functions import Coalesce

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'

    def __init__(self, expression):
        super().__init__(expression, output_field=IntegerField())


def posts(request):
    category_query = request.GET.get('category')
    context = {'category_query': category_query}
    
    # Inicializar form y comment_form al principio
    form = PostForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        if "submit_post" in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.ranking = int(request.POST.get('ranking', 0)) if request.POST.get('ranking', 0).isdigit() else 0
                post.save()
                return redirect('posts')
        elif "submit_comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.post = Post.objects.get(id=request.POST.get("post_id"))
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comment.parent = Comment.objects.get(id=parent_id)
                comment.save()
                return redirect('posts')

    else:
        form = PostForm()
        comment_form = CommentForm()
    
    # Prepares posts with likes and star ratings for the template
    likes_prefetch = Prefetch('likes', queryset=Like.objects.filter(user=request.user), to_attr='current_user_like')
    all_posts = Post.objects.prefetch_related(likes_prefetch).order_by('-date_posted')
    if category_query:
        all_posts = all_posts.filter(category__name__icontains=category_query)

    for post in all_posts:
        post.is_liked = bool(post.current_user_like)
        post.star_ratings = get_star_ratings(post.ranking)
        post.top_level_comments = post.comments.filter(parent=None)

    context.update({
        'posts': all_posts,
        'form': form,
        'comment_form': comment_form,
    })

    return render(request, 'posts.html', context)

def toggle_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True

    return JsonResponse({"is_liked": is_liked, "likes_count": post.likes.count()})

def get_star_ratings(rating):
    # Esta función devuelve una lista de estrellas según el rating
    stars = []
    # Asegúrate de que el rating no sea None antes de hacer la comparación
    if rating is None:
        rating = 0  # O cualquier lógica que decidas para manejar un rating no establecido
    for i in range(1, 6):
        if rating >= i:
            stars.append('full')
        elif rating >= i - 0.5:
            stars.append('half')
        else:
            stars.append('empty')
    return stars