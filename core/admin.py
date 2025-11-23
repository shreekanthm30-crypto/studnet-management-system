from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'class_associated', 'teacher']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'class_enrolled']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'teacher_id']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'date', 'status']

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks_obtained', 'total_marks']

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['class_associated', 'day', 'subject', 'start_time']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'important']