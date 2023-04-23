from django.shortcuts import render, redirect
from boats.models import Boat
from .models import Cart


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    boat_id = request.POST.get('boat_id')
    if boat_id is not None:
        try:
            boat_obj = Boat.objects.get(id=boat_id)
        except Boat.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if boat_obj in cart_obj.boats.all():
            cart_obj.boats.remove(boat_obj)
        else:
            cart_obj.boats.add(boat_obj) # cart_obj.products.add(product_id)
            request.session['cart_items'] = cart_obj.boats.count()
        # return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")