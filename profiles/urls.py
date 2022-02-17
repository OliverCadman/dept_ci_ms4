from django.urls import path
from .views import (ProfileView, edit_profile, upload_audio,
                    upload_unavailable_dates, get_users_unavailable_dates)

urlpatterns = [
    path('<str:user_name>', ProfileView.as_view(), name="profile"),
    path('edit_profile/<str:username>', edit_profile, name="edit_profile"),
    path("upload_audio/<str:username>", upload_audio, name="upload_audio"),
    path("upload_unavailability/<str:username>", upload_unavailable_dates, name="upload_unavailability"),
    path("get_users_unavailable_dates/<str:username>", get_users_unavailable_dates)
]