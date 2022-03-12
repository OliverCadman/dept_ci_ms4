from django.urls import path
from .views import DepListView, JobListView, post_job

urlpatterns = [
    path('find_a_dep', DepListView.as_view(), name="dep_list" ),
    path('find_a_job', JobListView.as_view(), name="job_list"),
    path("post_job", post_job, name="post_job")
]