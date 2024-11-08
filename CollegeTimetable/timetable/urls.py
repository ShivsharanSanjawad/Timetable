from django.urls import path
from .views import (
    LandingPageView, BranchView, DivisionView, BatchView, SubjectView,
    TeacherView, RoomView, StudentElectiveView, TimetableView,
    ConflictResolutionView, GenerateTimetableView
)

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('branch/', BranchView.as_view(), name='branch'),
    path('division/', DivisionView.as_view(), name='division'),
    path('batch/', BatchView.as_view(), name='batch'),
    path('subject/', SubjectView.as_view(), name='subject'),
    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('room/', RoomView.as_view(), name='room'),
    path('student-elective/', StudentElectiveView.as_view(), name='student_elective'),
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('conflict-resolution/', ConflictResolutionView.as_view(), name='conflict_resolution'),
    path('generate-timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
]