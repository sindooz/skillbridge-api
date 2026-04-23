from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('trainer', 'Trainer'),
        ('institution', 'Institution'),
        ('programme_manager', 'Programme Manager'),
        ('monitoring_officer', 'Monitoring Officer'),
    ]

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    institution = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Batch(models.Model):
    name = models.CharField(max_length=255)
    institution = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    

class BatchTrainer(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

class BatchStudent(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

class BatchInvite(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

class Session(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_at = models.DateTimeField(auto_now_add=True)                    