from django.urls import path

from orders.api import apis


urlpatterns = [
    path("api/order/create/", apis.complete_order_api),
]
