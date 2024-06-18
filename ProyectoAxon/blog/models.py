from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator, ValidationError

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        
    def __str__(self):
        return self.nombre
    
# Validador personalizado para el tamaño máximo del archivo en kilobytes
def validate_image_size(value):
    file_size = value.size
    max_size_kb = 1024  # Tamaño máximo permitido en kilobytes (por ejemplo, 1MB = 1024KB)
    if file_size > max_size_kb * 1024:  # Convertir kilobytes a bytes
        raise ValidationError(f"Tamaño máximo de imagen permitido es {max_size_kb} KB")
    
    
class Producto(models.Model):
    titulo = models.CharField(max_length=150)
    contenido = models.TextField()
    precio = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    imagen = models.ImageField(
        default='null',
        upload_to="productos",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),  # Validar la extensión del archivo
            validate_image_size,  # Validar el tamaño del archivo
        ]
    )
    creado = models.DateTimeField(auto_now_add=True)
    categorias = models.ManyToManyField(Categoria, blank=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-creado']
        
    def __str__(self):
        return self.titulo
    


class ElementoCarrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.titulo} (Usuario: {self.usuario.username})"


class DireccionEnvio(models.Model):
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    telefono = PhoneNumberField(region='CL', blank=True, null=True)  # Campo de teléfono adaptado para Chile
    correo = models.EmailField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Dirección de envío: {self.direccion}, {self.ciudad}, {self.codigo_postal}'


class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    elementos = models.ManyToManyField(ElementoCarrito, through='ElementoOrden')
    direccion_envio = models.OneToOneField(DireccionEnvio, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    nombre_usuario = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        telefono = self.direccion_envio.telefono if self.direccion_envio else "No disponible"
        correo = self.direccion_envio.correo if self.direccion_envio else "No disponible"
        return (
            f"Orden #{self.id} - Usuario: {self.usuario.username}, "
            f"Nombre: {self.nombre_usuario}, "
            f"Teléfono: {telefono}, "
            f"Correo: {correo}, "
            f"Total: {self.precio_total}"
        )

    def obtener_productos(self):
        productos = self.elementoorden_set.all()
        return ", ".join([f"{p.cantidad} x {p.producto.titulo}" for p in productos])



@receiver(post_save, sender=Orden)
def transferir_productos_carrito(sender, instance, created, **kwargs):
    if created:
        # Obtener el carrito del usuario
        carrito_usuario = ElementoCarrito.objects.filter(usuario=instance.usuario)

        # Crear una lista de elementos de orden para agregar a la orden
        elementos_orden = []
        for elemento_carrito in carrito_usuario:
            elemento_orden = ElementoOrden(
                orden=instance,
                producto=elemento_carrito.producto,
                cantidad=elemento_carrito.cantidad
            )
            elementos_orden.append(elemento_orden)

        # Crear todos los elementos de orden en una sola operación
        ElementoOrden.objects.bulk_create(elementos_orden)

        # Eliminar todos los elementos del carrito una vez transferidos a la orden
        carrito_usuario.delete()

class ElementoOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    elemento_carrito = models.ForeignKey(ElementoCarrito, on_delete=models.CASCADE, null=True)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        if self.elemento_carrito and self.elemento_carrito.producto:
            return f'{self.cantidad} x {self.elemento_carrito.producto.titulo} (Orden #{self.orden.id})'
        else:
            return f'{self.cantidad} x [Producto no disponible] (Orden #{self.orden.id})'