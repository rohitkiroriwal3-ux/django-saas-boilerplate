from django.urls import path
from .views import CreateAPIKeyView, ListAPIKeysView, RevokeAPIKeyView, SaaSDataView


urlpatterns = [
    path("orgs/<int:org_id>/keys/", CreateAPIKeyView.as_view()),
    path("orgs/<int:org_id>/keys/list/", ListAPIKeysView.as_view()),
    path("keys/<int:key_id>/revoke/", RevokeAPIKeyView.as_view()),
    path("saas/data/", SaaSDataView.as_view())
]
