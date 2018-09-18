
from django.urls import path, include

from .views import Index
from .views import UpdateStatus
from .views import IssueDetail
from .views import RegisterView
from .views import NoteAPI

app_name ='bugtracker'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('update/', UpdateStatus.as_view(), name='update_status'),
    path('api/note', NoteAPI.as_view(), name='note_api'),
    path('issue/<int:pk>', IssueDetail.as_view(), name='issue_detail'),
    path('register/', RegisterView.as_view(), name='register'),
]
