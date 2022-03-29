from django.urls import path
from .views import (DepListView, JobListView, delete_job, post_job,
                    register_interest, get_interested_members,
                    confirm_job_offer, EditJobView, delete_job, remove_offer)

"""
Job URLs
----------------

URL Routing for the Jobs App
"""


urlpatterns = [
    path('find_a_dep', DepListView.as_view(), name="dep_list"),
    path('find_a_job', JobListView.as_view(), name="job_list"),
    path("post_job", post_job, name="post_job"),
    path("edit_job/<int:job_id>", EditJobView.as_view(), name="edit_job"),
    path("delete_job/<int:job_id>", delete_job, name="delete_job"),
    path("register_interest/<int:job_id>/<str:username>",
         register_interest, name="register_interest"),
    path("remove_offer/<int:job_id>/<str:username>",
         remove_offer, name="remove_offer"),
    path("get_interested_members/<int:job_id>",
         get_interested_members, name="get_interested_members"),
    path("confirm_job_offer/<int:job_id>/<str:confirmed_user_username>",
         confirm_job_offer, name="confirm_job_offer")
]
