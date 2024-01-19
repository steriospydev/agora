from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dash.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('account', include('apps.account.urls')),
    path('supplier/', include('apps.supplier.urls')),
    path('order/', include('apps.order.urls')),
    path('payment/', include('apps.payment.urls')),
    path('product/', include('apps.product.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)