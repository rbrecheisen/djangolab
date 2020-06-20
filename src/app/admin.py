from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from app.models import Patient, Hospital


@admin.register(Patient)
class PatientAdmin(GuardedModelAdmin, SimpleHistoryAdmin):

    list_display = (
        'id',
        'research_id',
        'hospital',
        'patient_id',
        'last_name',
        'in_fix',
        'initials',
        'gender',
        'country_of_org',
        'dob',
        'dod',
    )

    ordering = ('last_name', )

    search_fields = (
        'research_id',
        'hospital',
        'patient_id',
        'last_name',
        'gender',
        'country_of_org',
        'dob',
        'dod',
    )


class HospitalAdmin(GuardedModelAdmin, SimpleHistoryAdmin):

    list_display = (
        'id',
        'name',
        'country_of_org',
    )

    ordering = ('name', )

    search_fields = (
        'name',
        'country_of_org',
    )
