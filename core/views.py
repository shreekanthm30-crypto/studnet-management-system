from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import *

def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    try:
        if user.profile.role == 'admin':
            context.update({
                'total_students': Student.objects.count(),
                'total_teachers': Teacher.objects.count(),
                'total_classes': Class.objects.count(),
                'recent_announcements': Announcement.objects.all()[:5]
            })
            template = 'dashboard_admin.html'
            
        elif user.profile.role == 'teacher':
            teacher = Teacher.objects.get(user=user)
            context.update({
                'my_subjects': teacher.subjects.all(),
                'total_students': Student.objects.count(),
                'my_classes': Class.objects.filter(subject__teacher=user).distinct()
            })
            template = 'dashboard_teacher.html'
            
        elif user.profile.role == 'student':
            student = Student.objects.get(user=user)
            context.update({
                'student': student,
                'attendance': Attendance.objects.filter(student=student)[:10],
                'marks': Mark.objects.filter(student=student)[:10],
                'timetable': Timetable.objects.filter(class_associated=student.class_enrolled)
            })
            template = 'dashboard_student.html'
            
        else:
            template = 'dashboard_base.html'
            
    except (Profile.DoesNotExist, Student.DoesNotExist, Teacher.DoesNotExist):
        template = 'dashboard_base.html'
    
    return render(request, template, context)

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def take_attendance(request, subject_id):
    if request.user.profile.role != 'teacher':
        messages.error(request, 'Only teachers can take attendance')
        return redirect('dashboard')
    
    subject = get_object_or_404(Subject, id=subject_id)
    students = Student.objects.filter(class_enrolled=subject.class_associated)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'student_{student.id}') == 'on'
            remarks = request.POST.get(f'remarks_{student.id}', '')
            
            Attendance.objects.update_or_create(
                student=student,
                subject=subject,
                date=date,
                defaults={'status': status, 'remarks': remarks}
            )
        
        messages.success(request, f'Attendance recorded for {subject.name}')
        return redirect('dashboard')
    
    return render(request, 'take_attendance.html', {
        'subject': subject,
        'students': students,
        'today': timezone.now().date()
    })

@login_required
def enter_marks(request, subject_id):
    if request.user.profile.role != 'teacher':
        messages.error(request, 'Only teachers can enter marks')
        return redirect('dashboard')
    
    subject = get_object_or_404(Subject, id=subject_id)
    students = Student.objects.filter(class_enrolled=subject.class_associated)
    
    if request.method == 'POST':
        exam_date = request.POST.get('exam_date')
        total_marks = request.POST.get('total_marks', 100)
        
        for student in students:
            marks_obtained = request.POST.get(f'marks_{student.id}')
            if marks_obtained:
                Mark.objects.update_or_create(
                    student=student,
                    subject=subject,
                    exam_date=exam_date,
                    defaults={
                        'marks_obtained': marks_obtained,
                        'total_marks': total_marks,
                        'remarks': request.POST.get(f'remarks_{student.id}', '')
                    }
                )
        
        messages.success(request, f'Marks entered for {subject.name}')
        return redirect('dashboard')
    
    return render(request, 'enter_marks.html', {
        'subject': subject,
        'students': students,
        'today': timezone.now().date()
    })

@login_required
def view_attendance(request):
    if request.user.profile.role != 'student':
        messages.error(request, 'Only students can view attendance')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, user=request.user)
    attendance = Attendance.objects.filter(student=student).order_by('-date')
    
    return render(request, 'view_attendance.html', {
        'student': student,
        'attendance': attendance
    })

@login_required
def view_marks(request):
    if request.user.profile.role != 'student':
        messages.error(request, 'Only students can view marks')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, user=request.user)
    marks = Mark.objects.filter(student=student).order_by('-exam_date')
    
    return render(request, 'view_marks.html', {
        'student': student,
        'marks': marks
    })

@login_required
def view_timetable(request):
    if request.user.profile.role != 'student':
        messages.error(request, 'Only students can view timetable')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, user=request.user)
    timetable = Timetable.objects.filter(class_associated=student.class_enrolled).order_by('day', 'start_time')
    
    return render(request, 'view_timetable.html', {
        'student': student,
        'timetable': timetable
    })

@login_required
def announcements(request):
    announcements_list = Announcement.objects.all().order_by('-created_at')
    return render(request, 'announcements.html', {
        'announcements': announcements_list
    })