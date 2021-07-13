from django.contrib import admin

from orders.models import Order, PaymentMethod


admin.site.register(Order)
admin.site.register(PaymentMethod)
