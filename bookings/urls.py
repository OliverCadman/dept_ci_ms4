from django.urls import path
from .views import invitation_form_view

urlpatterns = [
    path('invitation', invitation_form_view, name="invitation"),
]