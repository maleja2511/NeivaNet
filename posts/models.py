from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def average_ranking(self):
        posts = Post.objects.filter(category=self)
        total_ranking = sum([post.ranking for post in posts if post.ranking is not None])
        count = posts.filter(ranking__isnull=False).count()
        return total_ranking / count if count > 0 else 0

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    ranking = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.title
    
    def has_user_liked(self, user):
        return self.likes.filter(user=user).exists()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"
    
    def get_all_replies(self):
        replies = list(self.replies.all())
        for reply in self.replies.all():
            replies.extend(reply.get_all_replies())
        return replies

    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']
