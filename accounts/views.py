from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from .tokens import email_verification_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from .serializers import SignupSerializer
from django.utils.http import urlsafe_base64_encode


User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        return HttpResponse("Invalid link")

    if email_verification_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return HttpResponse("Email verified successfully 🎉")
    else:
        return HttpResponse("Invalid or expired token")


class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user)

            verify_url = f"http://127.0.0.1:8000/verify/{uid}/{token}/"

            send_mail(
                "Verify your email",
                f"Click this link to verify: {verify_url}",
                "no-reply@saas.com",
                [user.email],
            )

            return Response(
                {"message": "Account created. Check email to verify."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)