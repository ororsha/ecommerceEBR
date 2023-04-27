import decimal

from django.shortcuts import render, redirect
from orders.models import Order
from boats.models import Boat
from booking.models import Booking
from .models import Cart
from datetime import datetime, timedelta
from django.http import Http404
from django.utils import timezone
import pytz


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    print(cart_obj)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    user =  request.POST.get('user_name')
    boat_id = request.POST.get('boat_id')

    if boat_id is not None:
        try:
            boat_obj    = Boat.objects.get(id=boat_id)
            booking_obj = add_booking(request, boat_obj)
        except Boat.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if booking_obj in cart_obj.booking.all():
            cart_obj.booking.remove(booking_obj) # remove from cart
            booking_obj.delete() # delete from booking
        else:
            cart_obj.booking.add(booking_obj) # cart_obj.booking.add(product_id)
            print(cart_obj.booking)
            request.session['cart_items'] = cart_obj.booking.count()
        # return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")


def add_booking(request, item):
    vessel_book = Booking.objects.filter(boat=item)
    start_date = request.session['invited_date']
    start_date = datetime.strptime(start_date[0:19], "%Y-%m-%dT%H:%M")
    return_date = request.session['return_date']
    return_date = datetime.strptime(return_date[0:19], "%Y-%m-%dT%H:%M")
    avilable_date = True

    # Check if date is valid
    min_rental_time = 3
    min_range = start_date + timedelta(hours=min_rental_time)

    # Check if minimum rental time is valid
    if min_range <= return_date:
        print("OK more then 3 hours")

        for i in vessel_book:
            if i.invited_date < pytz.utc.localize(start_date) < i.return_date:
                avilable_date = False

        if avilable_date:
            hours = return_date - start_date
            total_price = multiplication_hours(str(hours), item.get_price_per_hour())
            booking, created = Booking.objects.get_or_create(
                boat=item,
                user=request.user,
                ordered=False,
                invited_date=start_date,
                return_date=return_date,
                price=total_price
            )
            return booking
        else:
            raise Http404("already taken try another date")

    else:
        raise Http404("Less than 3 hours")


def multiplication_hours(hours, price):
    time_str = hours  # time format: hours:minutes:seconds
    hourly_rate = price  # dollars per hour

    # Convert the time string to a datetime object
    time_obj = datetime.strptime(time_str, '%H:%M:%S')

    # Convert the time to a number of hours
    num_hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600

    # Calculate the total earned
    total_earned = hourly_rate * decimal.Decimal(num_hours)

    print(f"Total cost: ${total_earned}")

    return total_earned


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.booking.count() == 0:
        return redirect("cart:home")
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request, "carts/checkout.html", {"object": order_obj})