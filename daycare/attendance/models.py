from django.db import models
from django.utils import timezone
# Adjust this import based on your actual Child model location
from children.models import Child 

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('ABSENT', 'Absent'),
        ('PRESENT', 'Present'),
        ('LEAVE', 'On Leave'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ABSENT')
    
    # Fields for Invoice Calculation later
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures a child cannot have two records for the same date
        unique_together = ('child', 'date')
        ordering = ['child'] # Adjust based on Child name field

    def __str__(self):
        return f"{self.child} - {self.date} - {self.status}"