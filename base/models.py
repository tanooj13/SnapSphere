from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default_profile_picture.jpg')
    bio = models.TextField(blank=True, null=True)

class Snap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snaps')
    image = models.ImageField(upload_to='snaps/')
    description = models.TextField()
    category = models.CharField(max_length=255, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    
    likes_count = models.PositiveIntegerField(default=0)  # Optimized
    comments_count = models.PositiveIntegerField(default=0)  # Optimized

    def update_likes_count(self):
        self.likes_count = self.likes.count()
        self.save(update_fields=['likes_count'])

    def update_comments_count(self):
        self.comments_count = self.comments.count()
        self.save(update_fields=['comments_count'])

class Like(models.Model):
    snap = models.ForeignKey(Snap, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('snap', 'user')  # Prevent duplicate likes

class Comment(models.Model):
    snap = models.ForeignKey(Snap, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SavedSnap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_snaps')
    snap = models.ForeignKey(Snap, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'snap')  # Prevent duplicate saves
