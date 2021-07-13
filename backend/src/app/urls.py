from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('billing.urls')),
    path('', include('carts.urls')),
    path('', include('categories.urls')),
    path('', include('courses.urls')),
    path('', include('discounts.urls')),
    path('', include('orders.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
