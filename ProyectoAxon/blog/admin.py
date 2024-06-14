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
    list_display = ('usuario', 'direccion_envio', 'mostrar_productos', 'fecha_creacion', 'precio_total')

    def mostrar_productos(self, obj):
        # Obtenemos los elementos de la orden
        elementos_orden = obj.elementoorden_set.all()
        
        # Creamos un conjunto para almacenar los productos únicos
        productos_unicos = set()
        
        # Creamos una lista para almacenar las cadenas de los productos únicos
        productos_unicos_str = []
        
        # Iteramos sobre los elementos de la orden
        for elemento in elementos_orden:
            # Creamos una cadena para representar el elemento actual
            producto_str = f"{elemento.cantidad} x {elemento.producto.titulo}"
            
            # Si la cadena del producto no está en el conjunto de productos únicos, la agregamos a la lista y al conjunto
            if producto_str not in productos_unicos:
                productos_unicos.add(producto_str)
                productos_unicos_str.append(producto_str)
        
        # Retornamos la lista de cadenas de productos únicos como una cadena separada por comas
        return ", ".join(productos_unicos_str)
    
    mostrar_productos.short_description = 'Productos'


class DireccionEnvioAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'ciudad', 'codigo_postal', 'telefono', 'correo')


# Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ElementoCarrito)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(DireccionEnvio, DireccionEnvioAdmin)