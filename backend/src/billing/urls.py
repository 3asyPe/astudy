from django.urls import path

from billing.api import apis


urlpatterns = [
    path('api/billing/get/', apis.get_billing_profile_api)
]

