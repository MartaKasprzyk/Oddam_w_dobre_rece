from django.contrib import admin

from oddam_app.models import Institution


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'type']


admin.site.register(Institution, InstitutionAdmin)
