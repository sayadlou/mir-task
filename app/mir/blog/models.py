from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
User = get_user_model()


class Post(models.Model):
    """"
    Model for save Article in blog app
    """

    class PostStatus(models.TextChoices):
        """"
        defined Choices for Post status
        """
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)
    content = models.TextField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_datetime = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=PostStatus.choices, max_length=10, default=PostStatus.OFFLINE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    @classmethod
    def get_online_posts(cls):
        # get all posts which have online status code
        return cls.objects.select_related("owner").filter(status=cls.PostStatus.ONLINE)

    def get_absolute_url(self):
        # get address of post in url
        return reverse('article', kwargs={'slug': self.slug, 'id': self.id})

    def save(self, *args, **kwargs):
        # save method override for make slug from title of post
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
