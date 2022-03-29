from django.urls import path
from .views import IndexView

"""
Home URLS
------------------

URL Routing for Home App
"""

urlpatterns = [
    path('', IndexView.as_view(), name="home")
]
