from django.urls import path
from .views import ProfileView

urlpatterns = [
    path('<str:user_name>', ProfileView.as_view(), name="profile")
]