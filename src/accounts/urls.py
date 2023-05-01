from django.urls import pathfrom .views import (        AccountHomeView,        AccountEmailActivateView,        UserDetailUpdateView,        )urlpatterns = [    path('', AccountHomeView.as_view(), name='home'),    path('details/', UserDetailUpdateView.as_view(), name='user-update'),    path('email/confirm/<str:key>/', AccountEmailActivateView.as_view(), name='email-activate'),    path('email/resend-activation/', AccountEmailActivateView.as_view(), name='resend-activation'),]