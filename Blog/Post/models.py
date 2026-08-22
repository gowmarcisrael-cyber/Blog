from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    STATUS = (
        ('draft','brouillon'),
        ('published','publier'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    excerpt = models.TextField(blank=True)
    content = models.TextField()

    cover = models.ImageField(
        upload_to='blog/covers/',
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='draft'
    )

    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True,null=True)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        related_name='articles',
        on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name='liked_posts',
        )

    bookmarks = models.ManyToManyField(
        User,
        blank=True,
        related_name='bookmarked_posts',
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="posts",
        blank=True,
    )

    class Meta:
        ordering = ["published_at"]

    def save(self, *args,**kwargs):
        if not self.pk:
            super().save(*args,**kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.pk}')
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author} - {self.post}"

class Paragraph(models.Model):
 
    post = models.ForeignKey(
        Post,
        related_name='paragraphs',
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255,blank=True)
 
    text = models.TextField(blank=True)
 
    image = models.ImageField(
        upload_to='blog/paragraphs/',
        blank=True,
        null=True,
    )
 
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ['order']
 
    def __str__(self):
        return f"{self.post} — {self.order}"