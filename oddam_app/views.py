from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from oddam_app.models import Donation, Institution, Category
from django.db.models import Sum
from django.db import IntegrityError
from django.contrib.auth.models import User
import datetime
from .forms import ChangePasswordForm
from django.contrib import messages


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


class PasswordHandlingMixin:
    def validate_password(self, request, password):
        lst = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}',
               '[', ']', '|', '\\', ':', '"', ';', "'", '<', '>', '?', ',', '.', '/', '"']

        return (len(password) >= 8 and
                any(x for x in password if x.isupper()) and
                any(x for x in password if x.islower()) and
                any(x for x in password if x.isdigit()) and
                any(x for x in password if x in lst)
                )

    def password_set(self, request, user, password, password2, template, redirect_template):
        try:
            if password != password2:
                return render(request, template, {'error': 'Hasła różnią się! '
                                                           'Spróbuj ponownie.'})
            else:
                validated_password = self.validate_password(request, password)
                if validated_password:
                    user.set_password(password)
                    user.save()

                    return redirect(redirect_template)

                else:
                    error = ('Hasło musi mieć długość min. 8 znaków, zawierać dużą i małą literę, '
                             'cyfrę i znak spacjalny. Spróbuj ponownie.')

                    return render(request, template, {'error': error})

        except IntegrityError:
            error = 'Konto z podanym adresem e-mail już istnieje. Spróbuj ponownie.'
            return render(request, template, {'error': error})


class RegisterView(PasswordHandlingMixin, View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        username = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Konto o podanym adresie e-mail już istnieje. Spróbuj ponownie lub zaloguj się.")
            return render(request, 'register.html')
        else:
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username)
            messages.success(request, "Konto użytkownika zostało utworzone. Zaloguj się.")
            return self.password_set(request, user, password, password2, 'register.html', 'login')


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
        else:
            messages.error(request, "Logowanie nie powiodło się. Zarejestruj się lub spróbuj ponownie.")
            return render(request, 'register.html')


class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, "Poprawne wylogowanie.")
        return redirect('index')


class UserPageView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user).order_by('-is_taken', 'pick_up_date', 'created')
        return render(request, 'user_page.html', {'user': user, 'donations': donations})


class UserPageUpdateDonationView(UserPassesTestMixin, View):

    def test_func(self):
        user = self.request.user
        donation = Donation.objects.get(pk=self.kwargs['pk'])
        return donation.user == user

    def get(self, request, pk):
        donation = Donation.objects.get(pk=pk)
        return render(request, 'donation_update_status.html', {'donation': donation})

    def post(self, request, pk):
        donation = Donation.objects.get(pk=pk)
        update_status = request.POST.get('is_taken')
        donation.is_taken = update_status
        donation.save()

        return redirect('user_page')


class UserSettingsView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        return render(request, 'user_settings.html', {'user': user})

    def post(self, request):
        user = request.user
        new_first_name = request.POST.get('name')
        new_last_name = request.POST.get('surname')
        new_username = request.POST.get('email')
        password_old = request.POST.get('password_old')

        get_user = User.objects.get(pk=user.id)
        get_current_username = User.objects.get(username=user.username)

        if check_password(password_old, get_user.password):
            if User.objects.filter(username=new_username).exclude(username=get_current_username).exists():
                messages.error(request, "Konto o podanym adresie e-mail już istnieje. Spróbuj ponownie.")
            else:
                user.first_name = new_first_name
                user.last_name = new_last_name
                user.username = new_username
                user.save()
                messages.success(request, "Dane zostały zaktualizowane.")
        elif password_old == '':
            messages.error(request, "Nie wpisano hasła. Spróbuj ponownie.")
        else:
            messages.error(request, "Niepoprawne hasło.")
            logout(request)
            return redirect('login')
        return render(request, 'user_settings.html', {'user': user})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = ChangePasswordForm(user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        user = request.user
        form = ChangePasswordForm(user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Hasło zostało zmienione. Zaloguj się ponownie.")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('user_settings')


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
