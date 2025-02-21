import pytest
from django.urls import reverse, resolve
from payment.views import home, payment_page, index, success_page, create_checkout_session

@pytest.mark.parametrize("url_name,view_function", [
    ('home', home),
    ('payment', payment_page),
    ('index', index),
    ('success', success_page),
    ('create_checkout_session', create_checkout_session),
])
def test_urls_resolve_correctly(url_name, view_function):
    url = reverse(url_name)
    assert resolve(url).func == view_function
