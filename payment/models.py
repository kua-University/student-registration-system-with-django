from django.db import models
from django.conf import settings
import stripe

class Payment(models.Model):
    student_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    course_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.student_name} for {self.course_name}"

    class Meta:
        ordering = ['-created_at']