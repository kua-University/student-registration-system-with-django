import pytest
from unittest.mock import patch
from django.urls import reverse
from django.test import Client
from .models import Payment

@pytest.mark.django_db
def test_payment_form_displayed():
    """Test that the payment form is displayed correctly."""
    client = Client()
    response = client.get(reverse('payment_page'))  # Assuming 'payment_page' is the name of the payment form URL

    assert response.status_code == 200
    assert 'student_name' in response.content.decode()  # Check that the form field is present in the response
    assert 'course_name' in response.content.decode()  # Check that the form field is present in the response


@pytest.mark.django_db
@patch('stripe.PaymentIntent.create')  # Mock Stripe PaymentIntent API
def test_successful_payment(mock_payment_intent_create):
    """Test that a payment is created and saved when the form is submitted successfully."""

    # Mock the Stripe PaymentIntent creation
    mock_payment_intent_create.return_value = {
        'id': 'pi_test_12345',
        'status': 'succeeded'
    }

    client = Client()

    # Payment form data for a successful payment
    payment_data = {
        'student_name': 'John Doe',
        'email': 'john.doe@example.com',
        'course_name': 'Python Course',
        'amount': 100.00  # Payment amount in dollars
    }

    # Simulate a POST request to the payment page
    response = client.post(reverse('payment_page'), payment_data)

    # Verify that the payment is saved to the database
    payment = Payment.objects.first()
    assert payment is not None
    assert payment.student_name == 'John Doe'
    assert payment.course_name == 'Python Course'
    assert payment.amount == 100.00
    assert payment.stripe_payment_intent == 'pi_test_12345'

    # Verify successful redirect to the success page
    assert response.status_code == 302  # Redirect code
    assert response.url == reverse('success_page')  # Redirects to success page


@pytest.mark.django_db
@patch('stripe.PaymentIntent.create')  # Mock Stripe PaymentIntent API
def test_payment_failure(mock_payment_intent_create):
    """Test that payment failure is handled properly."""
    
    # Mocking Stripe PaymentIntent creation to simulate a failure
    mock_payment_intent_create.side_effect = Exception("Stripe error: Payment failed")

    client = Client()

    # Payment form data for a failed payment
    payment_data = {
        'student_name': 'John Doe',
        'email': 'john.doe@example.com',
        'course_name': 'JavaScript Course',
        'amount': 100.00
    }

    response = client.post(reverse('payment_page'), payment_data)

    # Assert that the error message is returned
    assert response.status_code == 200  # Form should still be shown on error
    assert 'error' in response.content.decode()  # Check if error is in the response content


@pytest.mark.django_db
def test_success_page():
    """Test the success page rendering after a successful payment."""
    client = Client()
    response = client.get(reverse('success_page'))

    # Check if success page renders correctly
    assert response.status_code == 200
    assert 'Payment Successful' in response.content.decode()  # Assuming this text appears on the success page


@pytest.mark.django_db
@patch('stripe.checkout.Session.create')  # Mock Stripe Checkout Session API
def test_create_checkout_session(mock_create_checkout_session):
    """Test the create_checkout_session view."""
    
    # Mock Stripe Checkout Session creation
    mock_create_checkout_session.return_value = {'url': 'http://localhost:8000/checkout_url/'}

    client = Client()

    # Simulate GET request to create checkout session
    response = client.get(reverse('create_checkout_session'))

    # Assert that we are redirected to the Stripe checkout page
    assert response.status_code == 302  # 302 redirect
    assert response.url == 'http://localhost:8000/checkout_url/'  # Check that the URL is correct


@pytest.mark.django_db
def test_home_page():
    """Test the home page rendering."""
    client = Client()
    response = client.get(reverse('home'))  # Assuming 'home' is the name of the home page URL

    assert response.status_code == 200
    assert 'Welcome to the payment system' in response.content.decode()  # Assuming this message appears


@pytest.mark.django_db
def test_index_page_with_payment_form():
    """Test the index page with the payment form."""
    client = Client()
    response = client.get(reverse('index'))  # Assuming 'index' is the name of the index page URL

    assert response.status_code == 200
    assert 'student_name' in response.content.decode()  # Check the payment form is present

