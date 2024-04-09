from django.shortcuts import render
from django.views import View

from oddam_app.models import Donation, Institution
from django.db.models import Sum


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
    def get(self, request):
        return render(request, 'register.html')
