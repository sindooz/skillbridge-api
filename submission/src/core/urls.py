from django.urls import path
from .views import SignupView, LoginView
from .views import CreateBatchView, GenerateInviteView, JoinBatchView
from .views import CreateSessionView,MonitoringTokenView, MonitoringAttendanceView
from .views import SessionAttendanceView, BatchSummaryView,InstitutionSummaryView,ProgrammeSummaryView

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('batches/', CreateBatchView.as_view()),
    path('batches/<int:batch_id>/invite/', GenerateInviteView.as_view()),
    path('batches/join/', JoinBatchView.as_view()),   
    path('sessions/', CreateSessionView.as_view()),
    path('sessions/<int:session_id>/attendance/', SessionAttendanceView.as_view()),
    path('batches/<int:batch_id>/summary/', BatchSummaryView.as_view()),
    path('institutions/<int:institution_id>/summary/', InstitutionSummaryView.as_view()),
    path('programme/summary/', ProgrammeSummaryView.as_view()),
    path('auth/monitoring-token/', MonitoringTokenView.as_view()),
    path('monitoring/attendance/', MonitoringAttendanceView.as_view())
]