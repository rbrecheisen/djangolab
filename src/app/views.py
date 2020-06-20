from rest_framework import generics, permissions
from app.models import Patient
from app.serializers import PatientSerializer
from app.permissions import MyDjangoModelPermissions
from app.utilities import set_current_user


class CurrentUserMixin(generics.GenericAPIView):

    """
    This mixin is responsible for catching the dispatch() method and making sure
    the request.user is set in the local thread. This allows our models to store
    the current user as the entity that modified the model.
    """

    def dispatch(self, request, *args, **kwargs):
        # try:
        r = self.initialize_request(request, *args, **kwargs)
        set_current_user(r.user)
        return super(CurrentUserMixin, self).dispatch(request, *args, **kwargs)
        # except RuntimeError as e:
        #     return {'error': repr(e)}


class PatientListCreateAPIView(CurrentUserMixin, generics.ListCreateAPIView):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (permissions.IsAuthenticated, MyDjangoModelPermissions, )


class PatientRetrieveUpdateDestroyAPIView(CurrentUserMixin, generics.RetrieveUpdateDestroyAPIView):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (permissions.IsAuthenticated, MyDjangoModelPermissions, )
