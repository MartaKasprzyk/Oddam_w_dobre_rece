from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from oddam_app.models import Donation, Institution, Category
from django.db.models import Sum
from django.db import IntegrityError
from django.contrib.auth.models import User


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


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all().order_by("name")
        context = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', context)


