from django.db import models
from django.utils import timezone

class Guardian(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    photo = models.ImageField(upload_to='guardians/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Child(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    CLASS_CHOICES = [
        ('Infants', 'Infants'),
        ('Toddlers', 'Toddlers'),
        ('Pre-K', 'Pre-K'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Left', 'Left'),
    ]

    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='children')
    full_name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    enrollment_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    start_date = models.DateField(default=timezone.now)
    photo = models.ImageField(upload_to='children/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    # Generate a simple ID like #1001
    def get_student_id(self):
        return f"#{1000 + self.id}"

    def __str__(self):
        return self.full_name