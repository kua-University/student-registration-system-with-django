import pytest
from payment.models import Payment

@pytest.mark.django_db
def test_create_payment():
    payment = Payment.objects.create(
        student_name="John Doe",
        email="john@example.com",
        course_name="Django Basics",
        amount=99.99,
        stripe_payment_intent="pi_123456789"
    )

    assert payment.student_name == "John Doe"
    assert payment.email == "john@example.com"
    assert payment.course_name == "Django Basics"
    assert payment.amount == 99.99
    assert payment.stripe_payment_intent == "pi_123456789"
    assert payment.created_at is not None
