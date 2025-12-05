from django.db import models
from django.utils import timezone

class StaffMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    ROLE_CHOICES = [
        ('Teacher', 'Teacher'),
        ('Assistant', 'Assistant'),
        ('Admin', 'Administrator'),
        ('Cleaner', 'Cleaning Staff'),
        ('Driver', 'Driver'),
        ('Security', 'Security'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('On Leave', 'On Leave'),
        ('Resigned', 'Resigned'),
    ]

    # Personal Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_spouse_name = models.CharField(max_length=100, verbose_name="Father/Spouse Name")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Contact Details
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # Job Details
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Teacher')
    date_joined = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monthly Salary")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"