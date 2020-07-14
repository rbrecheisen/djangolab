from uuid import uuid4
from django.db.models import Model, UUIDField, CharField, ForeignKey, BooleanField, SET_NULL
from simple_history.models import HistoricalRecords
from app.utilities import get_current_user


class Resource(Model):

    id = UUIDField(
        primary_key=True,
        blank=True
    )

    description = CharField(max_length=64)

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
        super(Resource, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.hidden = True
        self.changeReason = 'delete'
        self.save()
