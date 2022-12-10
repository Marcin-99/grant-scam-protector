from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class WhisperIntegrationView(GenericAPIView):
    def get(self, request):
        return Response({"success": True}, 200)
