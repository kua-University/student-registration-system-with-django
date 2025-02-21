import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Payment
from decouple import config
from django import forms

class PaymentForm(forms.Form):
    student_name = forms.CharField(label="student_name",max_length=255)
    email = forms.EmailField(label="Email")
    course_name = forms.CharField(label="course",max_length=255)
    amount = forms.DecimalField(label="amount",max_digits=10, decimal_places=2)
   


stripe.api_key = config('STRIPE_TEST_SECRET_KEY')

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def payment_page(request):
    if request.method == 'POST':
        student_name = request.POST['student_name']
        email = request.POST['email']
        course_name = request.POST['course_name']
        amount = float(request.POST['amount']) * 100  # Stripe requires amounts in cents

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency='usd',
                payment_method_types=['card'],
            )
            Payment.objects.create(
                student_name=student_name,
                email=email,
                course_name=course_name,
                amount=amount / 100,  # Store in dollars
                stripe_payment_intent=payment_intent['id'],
            )
            return redirect('success_page')  # Redirect to a success page
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'payment/payment_form.html', {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
          "form":PaymentForm()
    })


def success_page(request):
    return render(request, 'payment/success.html')


def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Java Course',
                    },
                    'unit_amount': 2000,  # Amount in cents
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return redirect(session.url, code=303)
def home(request):
    return render(request,"payment/home.html")
def index(request):
    return render(request,"payment/index.html",{
        "form":PaymentForm()
    })
