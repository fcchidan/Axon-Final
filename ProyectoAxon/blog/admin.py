from django.contrib import admin
from .models import Categoria, Producto, ElementoCarrito, Orden, DireccionEnvio, ElementoOrden

class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('creado',)
    search_fields = ('nombre', 'descripcion')


class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('usuario', 'creado',) 
    search_fields = ('titulo', 'contenido')  
    list_display = ('titulo', 'creado', 'precio') 
    list_filter = ('categorias',)
    
    def save_model(self, request, obj, form, change):
        if not obj.usuario_id:
            obj.usuario_id = request.user.id
        obj.save()



class OrdenAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_usuario', 'telefono_usuario', 'correo_usuario', 'direccion_envio', 'mostrar_productos', 'fecha_creacion', 'precio_total')
    search_fields = ('usuario__username', 'nombre_usuario', 'direccion_envio__telefono', 'direccion_envio__correo')
    list_filter = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)

    def telefono_usuario(self, obj):
        return obj.direccion_envio.telefono if obj.direccion_envio else "No disponible"

    def correo_usuario(self, obj):
        return obj.direccion_envio.correo if obj.direccion_envio else "No disponible"

    def mostrar_productos(self, obj):
        elementos_orden = obj.elementoorden_set.all()
        productos_unicos = set()
        productos_unicos_str = []
        
        for elemento in elementos_orden:
            producto_str = f"{elemento.cantidad} x {elemento.producto.titulo}"
            if producto_str not in productos_unicos:
                productos_unicos.add(producto_str)
                productos_unicos_str.append(producto_str)
        
        return ", ".join(productos_unicos_str)
    
    mostrar_productos.short_description = 'Productos'
    telefono_usuario.short_description = 'Teléfono'
    correo_usuario.short_description = 'Correo'


class DireccionEnvioAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'ciudad', 'codigo_postal', 'telefono', 'correo')




# Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ElementoCarrito)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(DireccionEnvio, DireccionEnvioAdmin)
# Ocultar el modelo completo
admin.site.unregister(ElementoCarrito)
admin.site.unregister(DireccionEnvio)