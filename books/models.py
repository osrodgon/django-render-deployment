from django.db import models
from categories.models import Category

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    date_published = models.DateField()
    
    categories = models.ManyToManyField(Category, related_name='categories')

    def __str__(self):
        return self.title