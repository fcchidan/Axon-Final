from django.db import models

# Create your models here.
class Page(models.Model):
    titulo = models.CharField(max_length=60)
    contenido = models.TextField()
    slug = models.CharField(unique=True, max_length=150, verbose_name="URL amigable")
    
    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"
        
    def __str__(self):
        return self.titulo