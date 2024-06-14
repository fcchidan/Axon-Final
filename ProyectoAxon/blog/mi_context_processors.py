from .models import ElementoCarrito

def total_productos_carrito(request):
    if request.user.is_authenticated:
        elementos_carrito = ElementoCarrito.objects.filter(usuario=request.user)
        total_productos_carrito = sum(item.cantidad for item in elementos_carrito)
    else:
        total_productos_carrito = 0
    return {'total_productos_carrito': total_productos_carrito}
