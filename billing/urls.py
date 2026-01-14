from django.urls import path
from .views import SubscribeView, UpgradePlanView

urlpatterns = [
    path("billing/<int:org_id>/subscribe/", SubscribeView.as_view()),
    path("<int:org_id>/upgrade/", UpgradePlanView.as_view()),
]
