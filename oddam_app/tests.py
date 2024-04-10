import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

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

def test_add_donation_view_get():
    url = reverse('add_donation')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200