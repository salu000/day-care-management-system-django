from django.db import models
from django.utils import timezone
from children.models import Child

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partially Paid'),
        ('PAID', 'Paid'),
    ]

    # Links
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='invoices')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    period_start = models.DateField(help_text="Billing period start")
    period_end = models.DateField(help_text="Billing period end")

    # Calculation Data
    total_days_present = models.IntegerField(default=0)
    daily_rate_applied = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Financials
    base_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Days * Rate")
    adjustment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Positive for extra charge, Negative for discount")
    adjustment_reason = models.CharField(max_length=255, blank=True, null=True)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID')

    def save(self, *args, **kwargs):
        # Auto-calculate total
        self.total_amount = float(self.base_amount) + float(self.adjustment_amount)
        
        # Auto-update status
        if self.amount_paid >= self.total_amount:
            self.status = 'PAID'
        elif self.amount_paid > 0:
            self.status = 'PARTIAL'
        else:
            self.status = 'UNPAID'
            
        super().save(*args, **kwargs)

    def get_balance_due(self):
        return self.total_amount - self.amount_paid

    def __str__(self):
        return f"INV-{self.id} - {self.child.full_name}"