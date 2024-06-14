from pages.models import Page

def get_pages(request):

    pages = Page.objects.values_list('titulo', 'slug')

    return {
        'pages': pages
    }