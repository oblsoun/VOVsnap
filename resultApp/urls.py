from django.urls import path
from . import views

app_name = 'resultApp'

urlpatterns = [
    path('danger/', views.danger_result_view, name='danger_result'),
    path('safe/', views.safe_result_view, name='safe_result'),
    path('send_email/', views.send_email, name='send_email'),
]