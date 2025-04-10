from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    TITLE_CHOICES = [
        ('announcement', 'Announcement'),
        ('blog', 'Blog'),
        ('celebration', 'Celebration'),
        ('post', 'Post'),
        ('write_up', 'Write-Up'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_type = models.CharField(max_length=20, choices=TITLE_CHOICES, default='post')  
    published_date = models.DateTimeField(null=True, blank=True)  # Only set if published
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)  # Tags for categorization
    is_published = models.BooleanField(default=False)  # To mark the post as published or draft
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Optional image upload

    class Meta:
        ordering = ['-created_at']  # Sort posts by creation date (newest first)

    def __str__(self):
        return self.title

    def publish(self):
        self.is_published = True
        self.published_date = timezone.now()
        self.save()

    def unpublish(self):
        self.is_published = False
        self.save()

    def is_recent(self):
        return self.created_at >= timezone.now() - timezone.timedelta(days=7) 


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=250)
    organizer = models.CharField(max_length=100)
    is_virtual = models.BooleanField(default=True)
    #attendees = models.ManyToManyField('User', related_name='events')
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=[('workshop', 'Workshop'), ('talk', 'Talk'), ('ctf', 'CTF')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def is_upcoming(self):
        return self.date > timezone.now()

    def is_past(self):
        return self.date < timezone.now()

    def register(self, user):
        self.attendees.add(user)
        self.save()
    
    def cancel(self):
        self.date = timezone.now()
        self.save()


    class Meta:
        ordering = ['-date']



