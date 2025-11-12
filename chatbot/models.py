# chatbot/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)         # ej: "Paneles solares"
    slug = models.SlugField(max_length=100, unique=True)         # ej: "paneles"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)                      # ej: "Panel Mono 450W"
    short_specs = models.CharField(max_length=255)               # ej: "Eficiencia 21.2%, 450W"
    image_url = models.URLField(blank=True)                      # usa CDN o ruta estática
    datasheet_url = models.URLField(blank=True)                  # link a PDF o ficha
    price_info = models.CharField(max_length=100, blank=True)    # ej: "$, rango estimado"

    def __str__(self):
        return self.name

