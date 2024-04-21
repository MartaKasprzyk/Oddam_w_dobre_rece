from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from oddam_app.models import Donation, Institution, Category
from django.db.models import Sum
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.http import JsonResponse
import datetime
import time


class LandingPageView(View):
    def get(self, request):
        total_quantity = Donation.objects.aggregate(total_quantity=Sum("quantity"))['total_quantity']
        supported_institutions = Donation.objects.values('institution').distinct().count()
        foundations = Institution.objects.filter(type=1)
        non_goverment_orgs = Institution.objects.filter(type=2)
        charity_fundraising = Institution.objects.filter(type=3)
        context = {
            'total_quantity': total_quantity,
            'supported_institutions': supported_institutions,
            'foundations': foundations,
            'non_goverment_orgs': non_goverment_orgs,
            'charity_fundraising': charity_fundraising
        }
        return render(request, 'index.html', context)


class RegisterView(View):
    def validate_password(self, request, password):
        lst = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}',
               '[', ']', '|', '\\', ':', '"', ';', "'", '<', '>', '?', ',', '.', '/', '"']

        return (len(password) >= 8 and
                any(x for x in password if x.isupper()) and
                any(x for x in password if x.islower()) and
                any(x for x in password if x.isdigit()) and
                any(x for x in password if x in lst)
                )

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        username = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        try:
            if password != password2:
                return render(request, 'register.html', {'error': 'Hasła różnią się! '
                                                                  'Spróbuj ponownie.'})
            else:
                validated_password = self.validate_password(request, password)
                if validated_password:
                    user = User.objects.create(first_name=first_name, last_name=last_name, username=username)
                    user.set_password(password)
                    user.save()

                    return redirect("login")

                else:
                    error = ('Hasło musi mieć długość min. 8 znaków, zawierać dużą i małą literę, '
                             'cyfrę i znak spacjalny. Spróbuj ponownie.')

                    return render(request, 'register.html', {'error': error})

        except IntegrityError:
            error = 'Konto z podanym adresem e-mail już istnieje. Spróbuj ponownie.'
            return render(request, 'register.html', {'error': error})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        url = request.GET.get('next', 'index')
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(url)
        return render(request, 'register.html', {'error': 'Nie ma takiego użytkownika. '
                                                          'Zarejestruj się.'})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class UserPageView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        return render(request, 'user_page.html', {'user': user})


class AddDonationView(LoginRequiredMixin, View):

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all().order_by("name")
        context = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', context)


class ConfirmationView(LoginRequiredMixin, View):
    def validate_postcode(self, request, zip_code):
      return len(zip_code) == 6 and zip_code[:1].isnumeric() and zip_code[2] == "-" and zip_code[3:].isnumeric()

    def validate_form(self, request, form_data):

        categories_ids = form_data.getlist('categories')
        categories_ids_num = [int(i) for i in categories_ids]
        categories = Category.objects.filter(pk__in=categories_ids_num)

        quantity = int(form_data['bags'])

        institution_id = form_data.get('organization')
        institution = Institution.objects.get(pk=institution_id)

        address = form_data['address']
        address = address.replace(" ", "")

        city = form_data['city']
        city = city.replace(" ", "")

        zip_code = form_data['postcode']
        validated_zip_code = self.validate_postcode(request, zip_code)

        phone_number = form_data['phone']

        pick_up_date = form_data['data']
        pick_up_date = datetime.date.fromisoformat(pick_up_date)

        pick_up_time = form_data['time']

        if len(categories) > 0:
            if quantity is not None and quantity > 0:
                if institution is not None:
                    if any(x for x in address if x.isalpha()) and any(x for x in address if x.isdigit()):
                        if city.isalpha():
                            if validated_zip_code:
                                if phone_number.isdigit():
                                    if pick_up_date > datetime.date.today():
                                        if pick_up_time:
                                            return True
        else:
            return False

    def get(self, request):
        return render(request, 'form-confirmation.html')

    def post(self, request):
        user = request.user
        form_data = request.POST
        institution_id = form_data.get('organization')
        institution = Institution.objects.get(pk=institution_id)
        categories_ids = form_data.getlist('categories')
        categories_ids_num = [int(i) for i in categories_ids]
        categories = Category.objects.filter(pk__in=categories_ids_num)

        validated = self.validate_form(request, form_data)

        if validated:
            donation = Donation.objects.create(quantity=form_data['bags'], institution=institution,
                                               address=form_data['address'], phone_number=form_data['phone'],
                                               city=form_data['city'], zip_code=form_data['postcode'],
                                               pick_up_date=form_data['data'], pick_up_time=form_data['time'],
                                               pick_up_comment=form_data['more_info'], user=user)
            donation.categories.set(categories)
            donation.save()
            return redirect('confirmation')

        return render(request, 'form.html')
