from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from organizations.models import Organization, Membership
from .models import Plan, Subscription
from django.shortcuts import get_object_or_404

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)

        if not Membership.objects.filter(user=request.user, organization=org, role="owner").exists():
            return Response({"error": "Only owner can subscribe"}, status=403)

        plan = get_object_or_404(Plan, name=request.data["plan"])

        Subscription.objects.update_or_create(
            organization=org,
            defaults={"plan": plan, "is_active": True}
        )

        return Response({"message": f"{org.name} subscribed to {plan.name}"})

class UpgradePlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)

        # Only owner can upgrade
        if not Membership.objects.filter(
            user=request.user, organization=org, role="owner"
        ).exists():
            return Response({"error": "Only owner can upgrade"}, status=403)

        plan_name = request.data.get("plan")

        try:
            new_plan = Plan.objects.get(name=plan_name)
        except Plan.DoesNotExist:
            return Response({"error": "Invalid plan"}, status=400)

        subscription = get_object_or_404(Subscription, organization=org, is_active=True)

        subscription.plan = new_plan
        subscription.save()

        return Response({
            "message": f"Upgraded to {new_plan.name}",
            "max_members": new_plan.max_members,
            "api_calls": new_plan.api_calls_per_month
        })
