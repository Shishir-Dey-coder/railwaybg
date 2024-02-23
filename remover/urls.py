from django.urls import path
from .views import upload_image, download_image ,home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home, name='home'),
    path('remove/', upload_image, name='remove'),
    #path('image_upload_success/', image_upload_success, name='image_upload_success'),
    path('download/<int:image_id>/', download_image, name='download_image'),
]

# Add the following line to serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
