from django.urls import path
from .views import JobPageView

urlpatterns = [
    path('<str:job_name>', JobPageView.as_view(), name="job_page")
]