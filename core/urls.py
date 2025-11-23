from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Teacher functions
    path('attendance/<int:subject_id>/', views.take_attendance, name='take_attendance'),
    path('marks/<int:subject_id>/', views.enter_marks, name='enter_marks'),
    
    # Student functions
    path('my-attendance/', views.view_attendance, name='view_attendance'),
    path('my-marks/', views.view_marks, name='view_marks'),
    path('my-timetable/', views.view_timetable, name='view_timetable'),
    path('announcements/', views.announcements, name='announcements'),
]