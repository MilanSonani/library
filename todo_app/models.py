from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    ROLE = (
        ('LIBRARIAN', 'Librarian'),
        ('MEMBER', 'Member')
    )

    role = models.CharField(max_length=15, choices=ROLE)#, default='MEMBER')
    username = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Book(models.Model):
    CHOICES = (
        ('BORROWED', 'Borrowed'),
        ('AVAILABLE', 'Available')
    )
    status = models.CharField(max_length=15, choices=CHOICES, default='AVAILABLE')
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class BorrowUserBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
