from django.urls import path
from . import views

app_name = 'loadingApp'

urlpatterns = [
    path('', views.loading_view, name='loading'),
    path('image_processing/', views.image_processing_view, name='image_processing'),
]
