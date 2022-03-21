from django.urls import path
from .views import (ProfileView, delete_account, edit_profile, upload_audio,
                    upload_unavailable_dates, get_users_unavailable_dates,
                    get_users_tracks, DashboardView, delete_account)

urlpatterns = [
    path('edit_profile', edit_profile, name="edit_profile"),
    path('<str:user_name>', ProfileView.as_view(), name="profile"),
    path("dashboard/<slug:slug>", DashboardView.as_view(), name="dashboard"),
    path("upload_audio/<str:username>", upload_audio, name="upload_audio"),
    path("get_users_unavailable_dates/<int:user_id>", get_users_unavailable_dates,
         name="get_users_unavailable_dates"),
    path("upload_unavailability/<int:user_id>", upload_unavailable_dates, name="upload_unavailability"),
    path("get_users_tracks/<int:user_id>", get_users_tracks, name="get_users_tracks"),
    path("delete_account/<int:profile_id>", delete_account, name="delete_account")
]