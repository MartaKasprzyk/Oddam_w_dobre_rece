import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from oddam_app.models import Donation, Category, Institution


@pytest.mark.django_db
def test_landing_page_view_get(donations):
    url = reverse('index')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['total_quantity'] == 3
    assert response.context['supported_institutions'] == 2


def test_login_view_get():
    url = reverse('login')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post_success(user):
    client = Client()
    url = reverse('login')
    data = {
        'email': user.username,
        'password': 'Password1@#'
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert response.context['user'] == user


@pytest.mark.django_db
def test_login_view_post_wrong_password(user):
    client = Client()
    url = reverse('login')
    data = {
        'email': user.username,
        'password': '12345'
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert response.context['error'] == 'Nie ma takiego użytkownika. Zarejestruj się.'


@pytest.mark.django_db
def test_login_view_post_wrong_username(user):
    client = Client()
    url = reverse('login')
    data = {
        'email': 'wrong_user@mail.com',
        'password': 'Password1@#'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert response.context['error'] == 'Nie ma takiego użytkownika. Zarejestruj się.'


@pytest.mark.django_db
def test_logout_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse("logout")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert not response.context['user'].is_authenticated


def test_register_view_get():
    url = reverse('register')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_register_view_post_passwords_different():
    client = Client()
    url = reverse('register')
    data = {
        'name': 'Name',
        'surname': 'Surname',
        'email': 'user@mail.com',
        'password': 'Password1@',
        'password2': 'aaaaaaa'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == "Hasła różnią się! Spróbuj ponownie."


@pytest.mark.django_db
def test_register_view_post_success():
    client = Client()
    url = reverse('register')
    data = {
        'name': 'Name',
        'surname': 'Surname',
        'email': 'user@mail.com',
        'password': 'Password1@',
        'password2': 'Password1@'
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    check_user = User.objects.get(first_name='Name', last_name='Surname', username="user@mail.com")
    assert check_user


@pytest.mark.django_db
def test_register_view_post_username_exists(user):
    client = Client()
    url = reverse('register')
    data = {
        'name': 'Name',
        'surname': 'Surname',
        'email': 'user@mail.com',
        'password': 'Password1@',
        'password2': 'Password1@'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == 'Konto z podanym adresem e-mail już istnieje. Spróbuj ponownie.'


@pytest.mark.django_db
def test_register_view_post_password_no_big_letter():
    client = Client()
    url = reverse('register')
    data = {
        'name': 'Name',
        'surname': 'Surname',
        'email': 'user@mail.com',
        'password': 'password1@',
        'password2': 'password1@'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == ('Hasło musi mieć długość min. 8 znaków, zawierać dużą i małą literę, '
                                         'cyfrę i znak spacjalny. Spróbuj ponownie.')


@pytest.mark.django_db
def test_register_view_post_password_no_small_letter():
    client = Client()
    url = reverse('register')
    data = {
        'name': 'Name',
        'surname': 'Surname',
        'email': 'user@mail.com',
        'password': 'PASSWORD1@',
        'password2': 'PASSWORD1@'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == ('Hasło musi mieć długość min. 8 znaków, zawierać dużą i małą literę, '
                                         'cyfrę i znak spacjalny. Spróbuj ponownie.')


@pytest.mark.django_db
def test_register_view_post_password_no_number():
    client = Client()
    url = reverse('register')
    data = {
        'name': 'Name',
        'surname': 'Surname',
        'email': 'user@mail.com',
        'password': 'Password#@',
        'password2': 'Password#@'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == ('Hasło musi mieć długość min. 8 znaków, zawierać dużą i małą literę, '
                                         'cyfrę i znak spacjalny. Spróbuj ponownie.')


@pytest.mark.django_db
def test_register_view_post_password_no_special_character():
    client = Client()
    url = reverse('register')
    data = {
        'name': 'Name',
        'surname': 'Surname',
        'email': 'user@mail.com',
        'password': 'Password11',
        'password2': 'Password11'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == ('Hasło musi mieć długość min. 8 znaków, zawierać dużą i małą literę, '
                                         'cyfrę i znak spacjalny. Spróbuj ponownie.')


@pytest.mark.django_db
def test_add_donation_view_get_success(user, categories, institutions):
    client = Client()
    client.force_login(user)
    url = reverse('add_donation')
    response = client.get(url)
    assert response.status_code == 200
    assert list(response.context['categories']) == categories
    assert list(response.context['institutions']) == institutions


def test_add_donation_view_get_not_logged():
    client = Client()
    url = reverse('add_donation')
    response = client.get(url, follow=True)
    assert response.status_code == 200

@pytest.mark.django_db
def test_confirmation_view_post_success(user, categories, institutions):
    client = Client()
    client.force_login(user)
    url = reverse('confirmation')
    data = {
        'categories': [categories[0].pk],
        'bags': 1,
        'organization': institutions[0].pk,
        'address': 'Ulica 12',
        'phone': 123456789,
        'city': 'City',
        'postcode': '00-111',
        'data': "2024-05-23",
        'time': '10:00:00',
        'more_info': 'comment',
        'user': user,
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Donation.objects.get(categories=categories[0],
                                quantity=1,
                                institution=institutions[0],
                                address='Ulica 12',
                                phone_number=123456789,
                                city='City',
                                zip_code='00-111',
                                pick_up_date="2024-05-23",
                                pick_up_time="10:00:00",
                                pick_up_comment='comment',
                                user=user
                                )
