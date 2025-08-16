# socialmedia_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Needed for static files in development
from django.conf.urls.static import static # Needed for static files in development

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # This tells Django to look for more URLs in our 'core' app
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
