import decimal
from django.conf import settings
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
from django.contrib import messages
from django.utils import timezone
import pytz

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY")
stripe.api_key = STRIPE_SECRET_KEY


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
            available_date, message = check_booking(request, boat_obj)

            if available_date:
                start_date, return_date = get_formatted_date(request)
                hours = return_date - start_date
                total_price = multiplication_hours(str(hours), boat_obj.get_price_per_hour())
                booked, created = Booking.objects.get_or_create(
                    boat=boat_obj,
                    user=request.user,
                    ordered=False,
                    invited_date=start_date,
                    return_date=return_date,
                    price=total_price
                )
                cart_obj.booking.add(booked)  # cart_obj.booking.add(product_id)
                request.session['cart_items'] = cart_obj.booking.count()
                print(request.session)
                messages.success(request, message)
            else:
                messages.info(request, message)
                return redirect("cart:home")

        else:
            print("Show message to user, product is gone?")
            return redirect("cart:home")

    # return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")


# Check if booking is available
def check_booking(request, item):
    vessel_book = Booking.objects.filter(boat=item)
    start_date, return_date = get_formatted_date(request)
    available_date = True

    # Check if date is valid
    min_rental_time = 3
    min_range = start_date + timedelta(hours=min_rental_time)

    # Check if minimum rental time is valid
    if min_range <= return_date:
        for i in vessel_book:
            if pytz.utc.localize(start_date) <= i.return_date and pytz.utc.localize(return_date) >= i.invited_date:
                available_date = False
                return available_date, "Already taken please choose another dates."

        if available_date:
            return available_date, "Amazing you can now pay for your cruse inside the cart."
    else:
        available_date = False
        return available_date, "Less than 3 hours, try another date."


def get_formatted_date(request):
    start_date = request.POST['invited_date']
    return_date = request.POST['return_date']
    start_date_formatted = datetime.strptime(start_date[0:19], "%Y-%m-%dT%H:%M")
    return_date_formatted = datetime.strptime(return_date[0:19], "%Y-%m-%dT%H:%M")

    return start_date_formatted, return_date_formatted


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
    has_card = False
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
        has_card = billing_profile.has_card

    if request.method == "POST":
        "check that order is done"
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                return redirect("cart:success")
            else:
                print(crg_msg)
                return redirect("cart:checkout")

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})