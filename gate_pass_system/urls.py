from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('internal-pass/', include('internal_pass.urls')),
    path('visitor-pass/', include('visitor_pass.urls')),
    path('helpdesk/', include('helpdesk.urls')),
    path('material-pass/', include('material_pass.urls')),
    path('grievance/', include('grievance.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
