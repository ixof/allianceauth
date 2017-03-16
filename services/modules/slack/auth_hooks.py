from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from services.hooks import ServicesHook
from alliance_auth import hooks

from .urls import urlpatterns
from .tasks import SlackTasks
from .models import SlackUser


class SlackService(ServicesHook):
    def __init__(self):
        ServicesHook.__init__(self)
        self.urlpatterns = urlpatterns
        self.name = 'slack'
        self.service_url = settings.SLACK_URL
        self.access_perm = 'slack.access_slack'

    @property
    def title(self):
        return "Slack"
        
    def invited(self, user):
        try:
            return bool(user.slack.invited)
        except ObjectDoesNotExist:
            return False
        
    def service_active_for_user(self, user):
        return user.has_perm(self.access_perm)
                
    def render_services_ctrl(self, request):
        urls = self.Urls()
        urls.auth_activate = 'auth_slack_invite'
        return render_to_string('registered/slack_service_ctrl.html', {
            'service_name': self.title,
            'urls': urls,
            'service_url': self.service_url,
            'invited': self.invited(request.user)
        }, request=request)


@hooks.register('services_hook')
def register_service():
    return SlackService()
