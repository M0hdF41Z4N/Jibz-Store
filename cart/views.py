from django.shortcuts import render,redirect,get_object_or_404
from demo.models import Product
from .models import Cart,Ord
from django.contrib import messages


# Create your views here.

#add to cart function
def add_to_cart(request,slug):
    item = get_object_or_404(Product,slug=slug)
    if not request.user.is_authenticated:
        messages.info(request,f"Please Login to add {item} in your cart")
        return redirect("account_login")
    order_item,created = Cart.objects.get_or_create(
    item = item,
    user = request.user
    )
    order_qs = Ord.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderItems.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,f"{item.name} quantity has updated.")
            return redirect("demo:cart-home")
        else:
            order.orderItems.add(order_item)
            messages.info(request,f"{item.name} is added to your cart.")
            return redirect("demo:demo")
    else:
        order = Ord.objects.create(
        user = request.user
        )
        order.orderItems.add(order_item)
        messages.info(request,f"{item.name} is added to your cart.")
        return redirect("demo:demo")



# Cart View function
def CartView(request):
    if not request.user.is_authenticated:
        messages.info(request,f"Please Login to continue.")
        return redirect("account_login")
    user = request.user
    carts = Cart.objects.filter(user=user)
    orders = Ord.objects.filter(user=user,ordered=False)
    if  orders.exists():    # Add  carts.exists() or
        order = orders[0]
        return render(request,'cart/home.html',{'carts':carts,'order':order})

    else:
        messages.warning(request,"You do not have any item in cart.")
        return redirect("demo:demo")

# remove from cart function
def remove_from_cart(request,slug):
    item = get_object_or_404(Product,slug=slug)
    order_qs = Ord.objects.filter(
    user=request.user,
    ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderItems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else :
                order.orderItems.remove(order_item)
                order_item.delete()
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("demo:cart-home")
        else:
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("demo:cart-home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("demo:cart-home")

# Remove Item from cart function
def decreaseCart(request,slug):
    item = get_object_or_404(Product,slug=slug)
    order_qs = Ord.objects.filter(
    user=request.user,
    ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderItems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            order.orderItems.remove(order_item)
            order_item.delete()
            messages.info(request, f"{item.name} removed from your cart.")
            return redirect("demo:cart-home")
        else:
            messages.info(request, f"You do not have {item.name} in your order.")
            return redirect("demo:demo")
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("demo:demo")
