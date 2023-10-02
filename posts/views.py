from django.shortcuts import redirect, render
from .models import Post
from .forms import PostForm

def posts(request):
    all_posts = Post.objects.all()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
    else:
        form = PostForm()

    context = {
        'posts': all_posts,
        'form': form
    }
    return render(request, 'posts.html', context)

