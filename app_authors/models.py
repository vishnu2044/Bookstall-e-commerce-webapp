from django.db import models


# Create your models here.


class Authors(models.Model):
    author_name = models.CharField(max_length=255)
    author_nation = models.CharField(max_length=255, null=True, blank=True)
    author_quotes = models.TextField(null=True, blank=True)
    author_description = models.TextField()
    author_image = models.ImageField(upload_to="phottos/authors", blank= True)
    author_birth_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'
    
    def __str__(self) -> str:
        return self.author_name

    # Rest of the model code

