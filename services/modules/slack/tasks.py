from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from notifications import notify

from .models import SlackUser


import logging

logger = logging.getLogger(__name__)


class SlackTasks:
    def __init__(self):
        pass

    @staticmethod
    def was_invited(user):
        try:
            return SlackUser(user).invited != ''
        except ObjectDoesNotExist:
            return False
    
    @staticmethod
    def invited(user):
        SlackUser.objects.update_or_create(user=user, defaults={'invited': True})