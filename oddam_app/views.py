from django.shortcuts import render, redirect
from django.views import View
from oddam_app.models import Donation, Institution
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


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


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
                    return render(request, 'register.html', {'error': 'Hasło musi mieć długość '
                                                                      'min. 8 znaków, zawierać dużą i małą literę,'
                                                                      'cyfrę i znak spacjalny. '
                                                                      'Spróbuj ponownie.'})

        except IntegrityError:
            return render(request, 'register.html', {'error': 'Konto z podanym adresem'
                                                              'e-mail już istnieje. Spróbuj ponownie.'})
