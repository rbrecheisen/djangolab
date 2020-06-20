from uuid import uuid4
from django.db.models import Model, UUIDField, CharField, DateField, ForeignKey, BooleanField, SET_NULL
from simple_history.models import HistoricalRecords
from app.utilities import COUNTRIES, create_research_id, get_current_user


########################################################################################################################
class Patient(Model):

    """
    This class represents a patient and records a few basic parameters such as
    last name, gender, date of birth and hospital ID.
    """
    # Set blank=True so we can leave the 'id' blank in the API
    # input form
    id = UUIDField(
        primary_key=True,
        blank=True,
    )

    # The research ID also has blank=True so we can leave it
    # blank in the API input form
    research_id = CharField(
        name='research_id',
        max_length=32,
        blank=True,
    )

    hospital = ForeignKey(
        'Hospital',
        name='hospital',
        on_delete=SET_NULL,
        null=True,
        blank=False,    # At least has to be unknown
        related_name='+',
    )

    patient_id = CharField(
        name='patient_id',
        max_length=32,
    )

    last_name = CharField(
        name='last_name',
        max_length=128,
    )

    in_fix = CharField(
        name='in_fix',
        max_length=8,
        default='',
        blank=True,
    )

    initials = CharField(
        name='initials',
        max_length=8,
        default='',
        blank=True,
    )

    gender = CharField(
        name='gender',
        max_length=1,
        choices=(
            ('M', 'Male'),
            ('F', 'Female'),
            ('T', 'Transgender'),
            ('U', 'Unknown'),
        )
    )

    country_of_org = CharField(
        name='country_of_org',
        max_length=30,
        choices=COUNTRIES,
        default='XX',
    )

    dob = DateField(name='dob')

    dod = DateField(
        name='dod',
        null=True,
        blank=True
    )

    # Keep track of who changed the patient model so we can log it in the
    # history. When the modified user gets deleted we keep the patient object
    # so the reference should be set to NULL
    modified_by = ForeignKey(
        'auth.User',
        name='modified_by',
        editable=False,
        related_name='+',
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    hidden = BooleanField(
        name='hidden',
        default=False,
    )

    deleted = BooleanField(
        name='deleted',
        default=False,
    )

    history = HistoricalRecords(
        history_id_field=UUIDField(default=uuid4),
    )

    @property
    def _history_user(self):
        return self.modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.modified_by = value

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.id = uuid4()
            self.research_id = create_research_id()
            self.changeReason = 'create'
        else:
            self.changeReason = 'update'
        current_user = get_current_user()
        if current_user:
            self.modified_by = current_user
        super(Patient, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.hidden = True
        self.changeReason = 'delete'
        self.save()

    def __str__(self):
        return '{}(id={},last_name={},patient_id={})'.format(
            self.__class__.__name__,
            self.id,
            self.last_name,
            self.patient_id,
        )


########################################################################################################################
class Hospital(Model):

    """
    This model represents a hospital entity.
    """
    id = UUIDField(
        primary_key=True,
        blank=True,
    )

    name = CharField(
        name='name',
        max_length=128,
    )

    country_of_org = CharField(
        name='country_of_org',
        max_length=30,
        choices=COUNTRIES,
        default='XX',
    )

    modified_by = ForeignKey(
        'auth.User',
        name='modified_by',
        editable=False,
        related_name='+',
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    hidden = BooleanField(
        name='hidden',
        default=False,
    )

    deleted = BooleanField(
        name='deleted',
        default=False,
    )

    history = HistoricalRecords(
        history_id_field=UUIDField(default=uuid4),
    )

    @property
    def _history_user(self):
        return self.modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.modified_by = value

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.id = uuid4()
            self.changeReason = 'create'
        else:
            self.changeReason = 'update'
        current_user = get_current_user()
        if current_user:
            self.modified_by = current_user
        super(Hospital, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.hidden = True
        self.changeReason = 'delete'
        self.save()

    def __str__(self):
        return '{}(id={},name={},country_of_org={})'.format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.country_of_org,
        )
