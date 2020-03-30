from django import template
from cart.models import Ord

register = template.Library()

@register.filter
def cart_total(user):
    order = Ord.objects.filter(user=user, ordered=False)

    if order.exists():
    	return order[0].orderItems.count()
    else:
    	return 0
