from __future__ import unicode_literals
from django.conf.urls import url, include

from . import views

module_urls = [
    # Slack Integration
    url(r'^invite/$', views.auth_slack_invite, name='auth_slack_invite'),
]

urlpatterns = [
    url(r'^slack/', include(module_urls)),
]
