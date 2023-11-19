from django.db import models


# Create your models here.


class ContactRequest(models.Model):
    """"
    model for save Contact request messages
    """
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=50)
    content = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
