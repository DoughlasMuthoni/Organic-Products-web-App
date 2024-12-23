from django.urls import path
from userAdmin import views

app_name = 'userAdmin'

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard")
]