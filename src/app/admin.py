from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from app.models import Resource


@admin.register(Resource)
class PatientAdmin(GuardedModelAdmin, SimpleHistoryAdmin):

    list_display = (
        'id',
    )

    ordering = ('id', )

    search_fields = (
    )
