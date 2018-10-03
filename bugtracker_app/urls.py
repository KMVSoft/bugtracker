
from django.urls import path, include

from .views import Index
from .views import UpdateStatus
from .views import IssueDetail
from .views import RegisterView
from .views import NoteAPI
from .views import ProfileView
from .views import SolvedIssuesView
from .views import InProgressIssuesView
from .views import ThanksForReporteView
from .views import ErrorAfterReportView

app_name ='bugtracker'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('update/', UpdateStatus.as_view(), name='update_status'),
    path('api/note', NoteAPI.as_view(), name='note_api'),
    path('issue/<int:pk>', IssueDetail.as_view(), name='issue_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('solved_issues/', SolvedIssuesView.as_view(), name='solved_issues'),
    path('in_progress_issues/', InProgressIssuesView.as_view(), name='in_progress_issues'),
    path('thanks/', ThanksForReporteView.as_view(), name='thanks_for_report'),
    path('error_after_report/', ErrorAfterReportView.as_view(), name='error_after_report'),
]
