from __future__ import unicode_literals
import random
import string
import requests
from eveonline.managers import EveManager
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from slackclient import SlackClient

from six import iteritems
from .tasks import SlackTasks

import logging

logger = logging.getLogger(__name__)


class SlackManager:
    def __init__(self):
        pass

    @classmethod
    def _response_ok(cls, response):
        try:
            if response['ok']:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def exec_request(endpoint, func, email, **kwargs):
        try:
            sc = SlackClient(settings.SLACK_TOKEN)
            res = sc.api_call('users.admin.invite', email=email, resend=True)
            return res
        except:
            logger.exception("Error encountered while performing API request to Slack.")
            return {}

    @classmethod
    def invite_user(cls, request):
        logger.debug("Inviting to Slack with email %s" % str(request.user.email))
        ret = SlackManager.exec_request('user', 'post', email=str(request.user.email))
        logger.debug(ret)
        if cls._response_ok(ret):
            logger.info("Invited to Slack (email): %s" % str(request.user.email))
            SlackTasks.invited(request.user)
            return True
        logger.info("Failed to invite Slack with email %s" % str(request.user.email))
        return None