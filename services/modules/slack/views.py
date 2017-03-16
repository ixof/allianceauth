from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .manager import SlackManager
from services.forms import ServicePasswordForm

import logging
logger = logging.getLogger(__name__)

ACCESS_PERM = 'slack.access_slack'


#@login_required
@permission_required(ACCESS_PERM)
def auth_slack_invite(request):
	logger.debug("activate_slack called by user %s" % request.user)
	SlackManager.invite_user(request)
	return render(request, 'registered/slack_invited.html', context={'service': 'Slack'})