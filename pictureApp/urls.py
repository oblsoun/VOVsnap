from django.urls import path
from . import views

app_name = 'pictureApp'

urlpatterns = [
    path('', views.picture_view, name='picture'),
    path('upload/', views.upload_image, name='upload'),
]