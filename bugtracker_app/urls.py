
from django.urls import path, include

from .views import Index
from .views import UpdateStatus

app_name ='bugtracker'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('update', UpdateStatus.as_view(), name='update_status'),
]
