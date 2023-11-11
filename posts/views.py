from django.shortcuts import redirect, render
from posts.models import Post, Like
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.db.models import Prefetch

def posts(request):
    category_query = request.GET.get('category')
    
    # Preparar la consulta prefetched de likes
    likes_prefetch = Prefetch('likes', queryset=Like.objects.filter(user=request.user), to_attr='current_user_like')

    if category_query:
        all_posts = Post.objects.filter(category__name__icontains=category_query).prefetch_related(likes_prefetch).order_by('-date_posted')
    else:
        all_posts = Post.objects.prefetch_related(likes_prefetch).order_by('-date_posted')

    # Añadir la propiedad is_liked a cada post
    for post in all_posts:
        post.is_liked = bool(post.current_user_like)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        comment_form = CommentForm(request.POST)

        if "submit_post" in request.POST and form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
        elif "submit_comment" in request.POST and comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = Post.objects.get(id=request.POST.get("post_id"))
            comment.save()
            return redirect('posts')
    else:
        form = PostForm()
        comment_form = CommentForm()

    context = {
        'posts': all_posts,
        'form': form,
        'comment_form': comment_form,
        'category_query': category_query
    }
    
    for post in all_posts:
        post.star_ratings = get_star_ratings(post.ranking)
        print(post.star_ratings)
        
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



