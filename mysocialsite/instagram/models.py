from django.contrib.staticfiles.views import serve
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} подписался {self.following}"


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="post/images/", blank=True, null=True)
    video = models.FileField(upload_to="post/videos/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hashtag = models.CharField(max_length=52, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Пост {self.user.username} на {self.created_at}"

class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="post_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.id}"

    # @classmethod
    # def toggle_like(cls, user, post):
    #     obj, created = cls.objects.get_or_create(user=user, post=post, defaults={"like": True})
    #     if not created:
    #         obj.delete()
    #         return None
    #     return obj

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments_post")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post}"

class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="comment_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.comment.id}"

    # @classmethod
    # def toggle_like(cls, user, comment):
    #     obj, created = cls.objects.get_or_create(user=user, comment=comment, defaults={"like": True})
    #     if not created:
    #         obj.delete()
    #         return None
    #     return obj


class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="stories")
    image = models.ImageField(upload_to="stories/images/", blank=True, null=True)
    video = models.FileField(upload_to="stories/videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

class UserSave(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_save')

    def __str__(self):
        return f"{self.user.username}"

class UserSaveItem(models.Model):
    post_item = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="saved_items")
    save_item = models.ForeignKey(UserSave, on_delete=models.CASCADE, related_name="items")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.post_item.id} - {self.save_item.user.username}"

class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)