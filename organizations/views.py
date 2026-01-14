from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Organization, Membership, Invitation
from .serializers import OrganizationSerializer
from django.shortcuts import get_object_or_404
from billing.models import Subscription
from .models import Invitation


class CreateOrganizationAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        org = Organization.objects.create(name=name, owner=request.user)
        Membership.objects.create(
            user=request.user,
            organization=org,
            role="owner"
        )
        return Response(OrganizationSerializer(org).data)

class InviteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)

        # Only owner or admin can invite
        if not Membership.objects.filter(
            user=request.user, organization=org, role__in=["owner", "admin"]
        ).exists():
            return Response({"error": "Not allowed"}, status=403)

        # 🔐 SaaS PAYWALL CHECK
        try:
            subscription = Subscription.objects.get(organization=org, is_active=True)
        except Subscription.DoesNotExist:
            return Response({"error": "No active subscription"}, status=400)

        plan = subscription.plan

        current_members = Membership.objects.filter(organization=org).count()
        pending_invites = Invitation.objects.filter(
            organization=org,
            is_accepted=False
        ).count()

        total_users = current_members + pending_invites

        if total_users >= plan.max_members:

            return Response({
                "error": "Plan limit reached",
                "plan": plan.name,
                "max_members": plan.max_members
            }, status=403)

        # Continue invite
        email = request.data["email"]
        role = request.data.get("role", "member")

        invite = Invitation.objects.create(
            email=email,
            organization=org,
            role=role,
        )

        return Response({
            "invite_link": f"http://127.0.0.1:8000/api/orgs/invites/{invite.token}/accept/"
        })



class AcceptInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, token):
        invite = get_object_or_404(Invitation, token=token, is_accepted=False)

        if request.user.email != invite.email:
            return Response({"error": "This invite is not for you"}, status=403)

        Membership.objects.create(
            user=request.user,
            organization=invite.organization,
            role=invite.role,
        )

        invite.is_accepted = True
        invite.save()

        return Response({"message": "You joined the organization"})
