from django.db.models import IntegerChoices
from django.utils.translation import gettext

class SourceType(IntegerChoices):
    Image = 0, gettext('Image')
    Video = 1, gettext('Video')
