from django.db import models
from django.utils import timezone
from children.models import Child

# --- EXISTING MODEL: Daily Activity Log (Tracker) ---
class DailyActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('MEAL', 'Meal / Snack'),
        ('NAP', 'Nap Time'),
        ('DIAPER', 'Diaper / Potty'),
        ('LEARNING', 'Learning / Activity'),
        ('PLAY', 'Play Time'),
        ('NOTE', 'General Note'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    title = models.CharField(max_length=100, help_text="e.g. Lunch, Afternoon Nap")
    description = models.TextField(blank=True, null=True, help_text="Details like 'Ate all food' or 'Slept 1 hour'")
    
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time'] # Newest first

    def __str__(self):
        return f"{self.child} - {self.get_activity_type_display()}"


# --- NEW MODEL: Class Schedule (Wireframe) ---
class ScheduleItem(models.Model):
    GROUP_CHOICES = [
        ('INFANT', 'Small (Infants)'),
        ('TODDLER', 'Medium (Toddlers)'),
        ('PRESCHOOL', 'Large (Preschoolers)'),
    ]

    THEME_CHOICES = [
        ('secondary', 'Grey (Standard)'),
        ('success', 'Green (Learning)'),
        ('info', 'Blue (Reading/Puzzle)'),
        ('primary', 'Dark Blue (Lunch)'),
        ('warning', 'Yellow (Departure)'),
    ]

    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='PRESCHOOL')
    start_time = models.TimeField()
    title = models.CharField(max_length=200, help_text="e.g. Learning Session")
    subtitle = models.CharField(max_length=200, blank=True, help_text="e.g. (Maths/ABC)")
    
    # Visual Styling
    color_theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='secondary')
    icon = models.CharField(max_length=50, default='bi-circle', help_text="Bootstrap Icon class, e.g. bi-book")

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.get_group_display()} - {self.start_time} - {self.title}"