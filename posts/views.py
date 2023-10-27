from django.shortcuts import redirect, render
from posts.models import Post, Like
from .forms import PostForm, CommentForm
from django.http import JsonResponse

def posts(request):
    all_posts = Post.objects.all().order_by('-date_posted')

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
        'comment_form': comment_form
    }
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