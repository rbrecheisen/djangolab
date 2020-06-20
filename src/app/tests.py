import requests
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from app.models import Patient, Hospital
from app.serializers import PatientSerializer, HospitalSerializer
from app.utilities import set_current_user


class BaseTest(LiveServerTestCase):

    def login(self, username='admin', password='secret'):
        email = '{}@me.com'.format(username)
        user = User.objects.filter(username=username).first()
        if not user:
            if username == 'admin':
                user = User.objects.create_superuser(username=username, password=password, email=email)
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
        set_current_user(user)
        self.client.login(username=username, password=password)
        return user


class BaseApiTest(BaseTest):

    # live_server_url = 'http://127.0.0.1:8000'

    def login(self, username='admin', password='secret'):
        email = '{}@me.com'.format(username)
        user = User.objects.filter(username=username).first()
        if not user:
            if username == 'admin':
                User.objects.create_superuser(username=username, password=password, email=email)
            else:
                User.objects.create_user(username=username, password=password, email=email)
        r = requests.post('{}/rest-auth/login/'.format(self.live_server_url), data={
            'username': username, 'password': password, 'email': email})
        token = r.json()[settings.TOKEN_KEY]
        return {'Authorization': '{} {}'.format(settings.TOKEN_SCHEMA, token)}


########################################################################################################################
class PatientModelTests(BaseTest):

    def setUp(self):
        self.request = self.login(username='admin')
        self.p = Patient.objects.create(
            last_name='Brecheisen', patient_id='12345', gender='M', dob='1973-07-16')

    @staticmethod
    def test_model_matches_serializer():
        # Purpose of this test is to verify that the fields in the model are
        # matched by the fields in the serializer. I'm explicitly testing this
        # because if they're not you get some pretty obscure errors that are
        # hard to debug.
        x = Patient._meta.get_fields()
        m_fields = []
        for f in x:
            m_fields.append(f.name)
        s_fields = PatientSerializer().fields
        for f in s_fields:
            if f not in m_fields:
                print('WARNING: Field {} in {} but not in {}'.format(
                    f,
                    PatientSerializer.__name__,
                    Patient.__name__,
                ))
        for f in m_fields:
            if f not in s_fields and f not in PatientSerializer.ignore_fields:
                print('WARNING: Field {} in {} but not in {}'.format(
                    f,
                    Patient.__name__,
                    PatientSerializer.__name__,
                ))

    def test_saving_patient_generates_uuid(self):
        self.assertIsNotNone(self.p.id)
        self.assertEqual(len(str(self.p.id)), 36)

    def test_saving_patient_generates_research_id(self):
        t = timezone.now()
        piece = 'P{}{}'.format(t.year, t.month)
        self.assertTrue(self.p.research_id.startswith(piece))

    def test_patient_has_history(self):
        self.assertEqual(len(self.p.history.all()), 1)

    def test_patient_has_history_user(self):
        h = self.p.history.first()
        self.assertEqual(h.history_user.username, 'admin')

    def test_patient_has_history_change_reason(self):
        h = self.p.history.first()
        self.assertIsNotNone(h.history_change_reason)
        self.assertEqual(h.history_change_reason, 'create')

    def test_history_can_be_reverted(self):
        # Update the patient and save it. You should now have 2 history items
        self.p.last_name = 'Coolsen'
        self.p.save()
        self.assertEqual(len(self.p.history.all()), 2)
        # Check that most recent history record has name 'Coolsen'
        self.assertEqual(self.p.history.first().instance.last_name, 'Coolsen')
        # Then revert back to the previous history record and verify that the
        # name has been reset to 'Brecheisen'
        h = self.p.history.first().prev_record
        p = h.instance
        p.save()
        self.assertEqual(p.last_name, 'Brecheisen')


class HospitalModelTests(BaseTest):

    def setUp(self):
        self.request = self.login(username='admin')
        self.h = Hospital.objects.create(name='mumc+', country_of_org='XX')

    @staticmethod
    def test_model_matches_serializer():
        # Purpose of this test is to verify that the fields in the model are
        # matched by the fields in the serializer. I'm explicitly testing this
        # because if they're not you get some pretty obscure errors that are
        # hard to debug.
        x = Hospital._meta.get_fields()
        m_fields = []
        for f in x:
            m_fields.append(f.name)
        s_fields = HospitalSerializer().fields
        for f in s_fields:
            if f not in m_fields:
                print('WARNING: Field {} in {} but not in {}'.format(
                    f,
                    HospitalSerializer.__name__,
                    Hospital.__name__,
                ))
        for f in m_fields:
            if f not in s_fields and f not in HospitalSerializer.ignore_fields:
                print('WARNING: Field {} in {} but not in {}'.format(
                    f,
                    Hospital.__name__,
                    HospitalSerializer.__name__,
                ))

    def test_create_patient_with_hospital(self):
        p = Patient.objects.create(
            last_name='Brecheisen',
            patient_id='12345',
            gender='M',
            dob='1973-07-16',
            hospital=self.h,
        )
        self.assertIsNotNone(p.hospital)
        self.assertEqual(p.hospital.name, 'mumc+')


########################################################################################################################
class PatientApiTests(BaseApiTest):

    def test_admin_can_view_patients(self):
        headers = self.login(username='admin')
        r = requests.get('{}/patients/'.format(self.live_server_url), headers=headers)
        self.assertEqual(r.status_code, 200, r.reason)

    def test_admin_can_create_change_and_delete_patients(self):
        headers = self.login(username='admin')
        r = requests.post(
            '{}/patients/'.format(self.live_server_url), data={
                'last_name': 'Brecheisen', 'patient_id': '12345', 'gender': 'M', 'dob': '1973-07-16'},
            headers=headers)
        self.assertEqual(r.status_code, 201, r.reason)

    def test_user_cannot_view_patients(self):
        headers = self.login(username='ralph')
        r = requests.get('{}/patients/'.format(self.live_server_url), headers=headers)
        self.assertEqual(r.status_code, 403, r.reason)
