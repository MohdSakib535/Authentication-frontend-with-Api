from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Student(AbstractUser):
    # Add any additional fields if needed
    student_id = models.CharField(max_length=10, unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups')
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions')
    )

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

