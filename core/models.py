from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Class(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    class_associated = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, 
                               limit_choices_to={'profile__role': 'teacher'},
                               related_name='teaching_subjects')
    
    def __str__(self):
        return f"{self.name} - {self.class_associated.name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE)
    parent_phone = models.CharField(max_length=15, blank=True)
    enrollment_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    subjects = models.ManyToManyField(Subject, blank=True,
                                     related_name='subject_teachers')
    hire_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.teacher_id}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student', 'subject', 'date']
    
    def __str__(self):
        status = "Present" if self.status else "Absent"
        return f"{self.student} - {self.subject} - {self.date} - {status}"

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    exam_date = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks_obtained}"

class Timetable(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    
    class_associated = models.ForeignKey(Class, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.class_associated} - {self.day} - {self.subject}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title