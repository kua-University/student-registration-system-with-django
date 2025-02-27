import pytest
from django.urls import reverse
<<<<<<< HEAD
=======
from django.conf import settings
>>>>>>> 6938dfa (i commit student payment system)
from django.test import Client
from .models import Payment
import stripe

# Mock Stripe API
@pytest.fixture
def mock_stripe_payment_intent(mocker):
    return mocker.patch('stripe.PaymentIntent.create', return_value={'id': 'test_intent'})

@pytest.fixture
def mock_checkout_session(mocker):
    return mocker.patch('stripe.checkout.Session.create', return_value={'url': 'http://localhost:8000/checkout'})

# Test Case 1: Test Payment Form Submission (POST)
@pytest.mark.django_db
<<<<<<< HEAD
def test_payment_page_post(client, mock_stripe_payment_intent):
=======
def test_payment_page_post(mock_stripe_payment_intent):
    client = Client()
>>>>>>> 6938dfa (i commit student payment system)
    data = {
        'student_name': 'John Doe',
        'email': 'john.doe@example.com',
        'course_name': 'Java Course',
        'amount': '100.00',
    }

    response = client.post(reverse('payment_page'), data)
    
    # Check if Payment Intent was created and Payment record is saved in the database
    payment_intent = stripe.PaymentIntent.create()
    assert Payment.objects.filter(stripe_payment_intent=payment_intent['id']).exists()

    # Check if user is redirected to the success page
    assert response.status_code == 302
    assert response.url == reverse('success_page')

<<<<<<< HEAD
# Test Case 2: Test Checkout Session Creation (POST)
@pytest.mark.django_db
def test_create_checkout_session_post(client, mock_checkout_session):
=======

# Test Case 2: Test Checkout Session Creation (POST)
@pytest.mark.django_db
def test_create_checkout_session_post(mock_checkout_session):
    client = Client()

>>>>>>> 6938dfa (i commit student payment system)
    response = client.post(reverse('create_checkout_session'))
    
    # Check if the Stripe session creation was called
    mock_checkout_session.assert_called_once()

    # Check if user is redirected to the Stripe checkout page
    assert response.status_code == 302
    assert response.url == 'http://localhost:8000/checkout'

<<<<<<< HEAD
# Test Case 3: Test Successful Payment Redirect
@pytest.mark.django_db
def test_success_page_get(client):
=======

# Test Case 3: Test Successful Payment Redirect
@pytest.mark.django_db
def test_success_page_get():
    client = Client()
>>>>>>> 6938dfa (i commit student payment system)
    response = client.get(reverse('success_page'))
    
    # Check that the success page renders correctly
    assert response.status_code == 200
    assert 'Payment Successful' in response.content.decode()
