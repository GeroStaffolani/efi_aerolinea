from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica el valor por el argumento"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def calculate_seat_price(precio_base, tipo_asiento):
    """Calcula el precio del asiento según su tipo"""
    try:
        precio = float(precio_base)
        if tipo_asiento == 'primera':
            return precio * 2
        elif tipo_asiento == 'ejecutiva':
            return precio * 1.5
        else:
            return precio
    except (ValueError, TypeError):
        return precio_base
