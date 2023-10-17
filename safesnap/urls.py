from django.contrib import admin
from django.urls import path, include
import mainApp.views
from django.conf.urls.static import static  
from safesnap import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainApp.views.main_view, name='main_view'),  
    path('picture/', include('pictureApp.urls')),
    path('loading/', include('loadingApp.urls')),
    path('result/', include('resultApp.urls')),
]

# 개발 중일 때만 미디어 파일 서빙을 추가
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_SAFE_URL, document_root=settings.MEDIA_SAFE_ROOT)
    urlpatterns += static(settings.MEDIA_DANGER_URL, document_root=settings.MEDIA_DANGER_ROOT)