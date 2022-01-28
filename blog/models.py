from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from account.models import UserData
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils.text import slugify

def upload_location(instance, filename, *args, **kwargs):
    file_path = 'post/{author_id}/{title}-{filename}'.format(author_id=str(instance.author.id), title=str(instance.title), filename=filename)
    return file_path


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
            

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to = upload_location,null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.title), slugify(self.author)))
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='user_comment')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)






