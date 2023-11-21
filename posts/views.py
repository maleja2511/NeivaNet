from django.shortcuts import redirect, render
from posts.models import Post, Like
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import Comment, Post, PostImage
from django.db.models import Func, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'

    def __init__(self, expression):
        super().__init__(expression, output_field=IntegerField())

@login_required
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
                # Guardar las imágenes
                for file in request.FILES.getlist('images'):
                    PostImage.objects.create(post=post, image=file)
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

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Asegúrate de que el usuario actual sea el autor de la publicación
    if request.user == post.author:
        post.delete()

    return redirect('posts')

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Asegúrate de que el usuario actual sea el autor del comentario o de la publicación
    if request.user == comment.user or request.user == comment.post.author:
        comment.delete()

    return redirect('posts')

def delete_reply(request, reply_id):
    reply = get_object_or_404(Comment, id=reply_id)

    # Asegúrate de que el usuario actual sea el autor de la respuesta o del comentario original o de la publicación        
    if request.user == reply.user or request.user == reply.parent.user or request.user == reply.post.author:
        reply.delete()
    
    return redirect('posts')

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

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.ranking = int(request.POST.get('ranking', 0)) if request.POST.get('ranking', 0).isdigit() else 0
                post.save()
                return redirect('posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def edit_comment(request):
    # Verificar si la solicitud es AJAX
    if request.method == 'POST' and request.accepts("application/json"):
        comment_id = request.POST.get('comment_id')
        new_content = request.POST.get('content')

        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.content = new_content
        comment.save()

        return JsonResponse({'message': 'Comentario actualizado correctamente.'})

    return JsonResponse({'message': 'Solicitud inválida.'}, status=400)