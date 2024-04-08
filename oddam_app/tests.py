import pytest
from django.test import Client
from django.urls import reverse

def test_landing_page_view_get():
    url = reverse('index')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200

def test_login_view_get():
    url = reverse('login')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200

def test_register_view_get():
    url = reverse('register')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200

def test_add_donation_view_get():
    url = reverse('add_donation')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200