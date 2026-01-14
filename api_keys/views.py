from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from organizations.models import Organization, Membership
from .models import APIKey
from .serializers import APIKeySerializer
from django.shortcuts import get_object_or_404
from .authentication import APIKeyAuthentication

class CreateAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)

        if not Membership.objects.filter(
            user=request.user,
            organization=org,
            role__in=["owner", "admin"]
        ).exists():
            return Response({"error": "Not allowed"}, status=403)

        name = request.data.get("name", "Default Key")

        key = APIKey.objects.create(
            organization=org,
            name=name
        )

        return Response(APIKeySerializer(key).data)


class ListAPIKeysView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)

        if not Membership.objects.filter(user=request.user, organization=org).exists():
            return Response({"error": "Not allowed"}, status=403)

        keys = APIKey.objects.filter(organization=org, is_active=True)
        return Response(APIKeySerializer(keys, many=True).data)


class RevokeAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, key_id):
        key = get_object_or_404(APIKey, id=key_id)

        if not Membership.objects.filter(
            user=request.user,
            organization=key.organization,
            role__in=["owner", "admin"]
        ).exists():
            return Response({"error": "Not allowed"}, status=403)

        key.is_active = False
        key.save()

        return Response({"message": "API key revoked"})


class SaaSDataView(APIView):
    authentication_classes = [APIKeyAuthentication]

    def get(self, request):
        return Response({
            "status": "success",
            "message": "This is protected SaaS data",
            "org": request.user.email
        })