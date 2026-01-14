from django.urls import path
from .views import InviteUserView, AcceptInviteView

urlpatterns = [
    path("orgs/<int:org_id>/invite/", InviteUserView.as_view()),
    path("orgs/invites/<uuid:token>/accept/", AcceptInviteView.as_view()),
]
