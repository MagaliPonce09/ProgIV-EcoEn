from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class Opinion(models.Model):
    nombre = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}: {self.mensaje[:30]}..."

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    es_cliente = models.BooleanField(default=True)
    es_vendedor = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)            # ✅ agregado
    website = models.URLField(blank=True, null=True)         # ✅ agregado

    def __str__(self):
        return f"{self.user.username} ({'Cliente' if self.es_cliente else 'Vendedor'})"
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/")
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    @property
    def promedio_puntuacion(self):
        puntuaciones = self.puntuaciones.all()
        if puntuaciones.exists():
            return round(sum(p.valor for p in puntuaciones) / puntuaciones.count(), 1)
        return 0


class Puntuacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='puntuaciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.PositiveSmallIntegerField()  # de 1 a 5
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'usuario')  # Un usuario solo puede puntuar una vez

    def __str__(self):
        return f"{self.usuario.username} → {self.producto.nombre}: {self.valor}⭐"


class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="simulado")

    def __str__(self):
        return f"{self.usuario.username} - {self.metodo_pago} - {self.total} ARS"

