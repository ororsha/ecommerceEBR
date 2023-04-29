import decimal
from django.shortcuts import render, redirect
from accounts.forms import LoginForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from boats.models import Boat
from booking.models import Booking
from .models import Cart
from datetime import datetime, timedelta
from django.http import Http404
from django.utils import timezone
import pytz


def cart_home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # print(cart_obj)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user =  request.POST.get('user_name')
    boat_id = request.POST.get('boat_id')
    booked_id = request.POST.get('item_id')
    print(booked_id)
    print(boat_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    if booked_id != "":
        booking_obj = Booking.objects.get(id=booked_id)
        cart_obj.booking.remove(booking_obj)  # remove from cart
        booking_obj.delete()  # delete from booking
    else:
        if boat_id != "":
            boat_obj = Boat.objects.get(id=boat_id)
            booking_obj, created = add_booking(request, boat_obj)
            cart_obj.booking.add(booking_obj)  # cart_obj.booking.add(product_id)
            request.session['cart_items'] = cart_obj.booking.count()
            print(request.session)
        else:
            print("Show message to user, product is gone?")
            return redirect("cart:home")

    # return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")

def add_booking(request, item):
    vessel_book = Booking.objects.filter(boat=item)
    start_date = request.POST['invited_date']
    start_date = datetime.strptime(start_date[0:19], "%Y-%m-%dT%H:%M")
    return_date = request.POST['return_date']
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
            return booking, created
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

    login_form = LoginForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        "check that order is done"
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})