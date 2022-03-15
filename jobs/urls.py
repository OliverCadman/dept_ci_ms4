from django.urls import path
from .views import DepListView, JobListView, post_job, register_interest, get_interested_members, confirm_job_offer

urlpatterns = [
    path('find_a_dep', DepListView.as_view(), name="dep_list" ),
    path('find_a_job', JobListView.as_view(), name="job_list"),
    path("post_job", post_job, name="post_job"),
    path("register_interest/<int:job_id>/<str:username>", register_interest, name="register_interest"),
    path("get_interested_members/<int:job_id>", get_interested_members),
    path("confirm_job_offer/<int:job_id>/<str:confirmed_user_username>", confirm_job_offer),
]