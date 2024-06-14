from blog.models import Categoria

def get_categoria(request):

    categorias = Categoria.objects.values_list('id', 'nombre')

    return {
        'categorias': categorias
    }