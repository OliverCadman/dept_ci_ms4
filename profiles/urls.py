from django.urls import path
from .views import (ProfileView, edit_profile, upload_audio,
                    upload_unavailable_dates, get_users_unavailable_dates,
                    get_users_tracks, DashboardView)

urlpatterns = [
    path('<str:user_name>', ProfileView.as_view(), name="profile"),
    path("dashboard/<str:username>", DashboardView.as_view(), name="dashboard"),
    path('edit_profile', edit_profile, name="edit_profile"),
    path("upload_audio/<str:username>", upload_audio, name="upload_audio"),
    path("get_users_unavailable_dates/<str:username>", get_users_unavailable_dates),
    path("upload_unavailability/<int:user_id>", upload_unavailable_dates, name="upload_unavailability"),
    path("get_users_tracks/<int:user_id>", get_users_tracks)
]