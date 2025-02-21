from django.test import TestCase
from payment.models import Payment

class PaymentModelTest(TestCase):
    def test_create_payment(self):
        payment = Payment.objects.create(
            student_name="John Doe",
            email="john@example.com",
            course_name="Django Basics",
            amount=99.99,
            stripe_payment_intent="pi_123456789"
        )

        self.assertEqual(payment.student_name, "John Doe")
        self.assertEqual(payment.email, "john@example.com")
        self.assertEqual(payment.course_name, "Django Basics")
        self.assertEqual(payment.amount, 99.99)
        self.assertEqual(payment.stripe_payment_intent, "pi_123456789")
        self.assertIsNotNone(payment.created_at)
