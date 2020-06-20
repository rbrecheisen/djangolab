from rest_framework.serializers import ModelSerializer
from app.models import Patient, Hospital


class PatientSerializer(ModelSerializer):

    ignore_fields = ('modified_by', 'hidden', 'deleted', )

    class Meta:
        model = Patient
        fields = (
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


class HospitalSerializer(ModelSerializer):

    ignore_fields = ('modified_by', 'hidden', 'deleted',)

    class Meta:
        model = Hospital
        fields = (
            'id',
            'name',
            'country_of_org',
        )
