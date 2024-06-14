from django import template

register = template.Library()

@register.filter(name='add_decimal_separator')
def add_decimal_separator(value):
    """
    A filter that adds decimal separator to a numeric value.
    """
    # Convierte el valor a cadena y divide los números antes y después del punto decimal
    parts = str(value).split('.')
    
    # Si hay parte decimal, agrega el punto decimal
    if len(parts) > 1:
        decimal_part = '.' + parts[1]
    else:
        decimal_part = ''
    
    # Formatea la parte entera con separadores de miles
    integer_part = '{:,}'.format(int(parts[0])).replace(',', '.')
    
    # Retorna la concatenación de la parte entera y la parte decimal
    return integer_part + decimal_part
