from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    # Model representing a Post
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blogpost_like', blank=True)
    category = models.ManyToManyField('Category', related_name="posts")

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        # String for representing the Model Object
        return self.title

    def number_of_likes(self):
        # Returns the number of likes on a post
        return self.likes.count()

    def get_fields(self):
        # Create a list of label/value pairs for columns
        return [(field.verbose_name, field.value_from_object(self))
                
            if field.verbose_name != 'post'
                
            else
                (field.verbose_name, 
                Post.objects.get(pk=field.value_from_object(self)).name)
                
            for field in self.__class__._meta.fields[1:]
        ]


class Comment(models.Model):
    # Model representing a Comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        # String for representing the Model Object
        return f"Comment {self.body} by {self.name}"


class Category(models.Model):
    # Model representing a Category of Posts
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        # String for representing the Model Object
        return self.title
