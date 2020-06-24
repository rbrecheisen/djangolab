import requests
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.conf import settings
from app.models import Resource
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
class ResourceModelTests(BaseTest):

    def setUp(self):
        self.request = self.login(username='admin')
        self.p = Resource.objects.create(description='Bla')

    def test_saving_patient_generates_uuid(self):
        self.assertIsNotNone(self.p.id)
        self.assertEqual(len(str(self.p.id)), 36)

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
        self.p.description = 'Blabla'
        self.p.save()
        self.assertEqual(len(self.p.history.all()), 2)
        # Check that most recent history record has name 'Coolsen'
        self.assertEqual(self.p.history.first().instance.description, 'Blabla')
        # Then revert back to the previous history record and verify that the
        # name has been reset to 'Bla'
        h = self.p.history.first().prev_record
        p = h.instance
        p.save()
        self.assertEqual(p.last_name, 'Bla')


########################################################################################################################
class PatientApiTests(BaseApiTest):

    def test_admin_can_view_patients(self):
        headers = self.login(username='admin')
        r = requests.get('{}/resources/'.format(self.live_server_url), headers=headers)
        self.assertEqual(r.status_code, 200, r.reason)

    def test_admin_can_create_change_and_delete_patients(self):
        headers = self.login(username='admin')
        r = requests.post(
            '{}/resources/'.format(self.live_server_url), data={'description': 'Bla'},
            headers=headers)
        self.assertEqual(r.status_code, 201, r.reason)

    def test_user_cannot_view_patients(self):
        headers = self.login(username='ralph')
        r = requests.get('{}/resources/'.format(self.live_server_url), headers=headers)
        self.assertEqual(r.status_code, 403, r.reason)
