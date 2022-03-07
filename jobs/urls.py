from django.urls import path
from .views import JobPageView, FindADepLandingPageView

urlpatterns = [
    path('find_a_dep', FindADepLandingPageView.as_view(), name="find_a_dep_landing_page" ),
    path('<str:job_name>', JobPageView.as_view(), name="job_page"),
]