from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    image_embedding = models.JSONField()  # Store CLIP embeddings
