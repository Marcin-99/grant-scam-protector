from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .utils.Audio_to_text import audio_to_text
from .utils.GPT import get_gpt_summary
from .models import SuspiciousKeyword, AlertMessage
from django.core import serializers


class WhisperIntegrationView(GenericAPIView):
    def post(self, request):
        phone_call = request.FILES.get('phoneCall')
        all_phone_call_text = audio_to_text(phone_call)

        # now calculations
        suspicious_keywords = {
            "Investigator": 0.3,
            "speaking": 1,
            "yes": 1,
            "give": 0.1,
        }

        keywords_that_occured_in_call = [
            {"keyword": key, "weight": value} for key, value in suspicious_keywords.items()
            if key in all_phone_call_text or key.lower() in all_phone_call_text
        ]

        allWeight = 0
        for keyword in keywords_that_occured_in_call:
            allWeight += keyword["weight"]

        if allWeight == 0:
            summaryItemColor = "#03fc28"
        elif 0 < allWeight < 1:
            summaryItemColor = "#f4fc03"
        elif 1 < allWeight < 2:
            summaryItemColor = "#fcb103"
        elif 3 < allWeight < 4:
            summaryItemColor = "#fc5603"
        elif 4 < allWeight:
            summaryItemColor = "#fc0303"

        #send to all_phone_call_text to pgt
        summary = get_gpt_summary(all_phone_call_text)

        #save everything
        alertMessage = AlertMessage(
            fullText=all_phone_call_text,
            summary=summary,
            summaryItemColor=summaryItemColor,
        )
        alertMessage.save()

        for keyword in keywords_that_occured_in_call:
            print(keyword["keyword"])
            print(keyword["weight"])
            obj = SuspiciousKeyword(keyword=keyword["keyword"], weight=keyword["weight"], alertMessage=alertMessage)
            obj.save()

        return Response({"success": True}, 200)


class AlertsView(GenericAPIView):
    def get(self, request):
        alerts = AlertMessage.objects.all()
        data = serializers.serialize('json', alerts)
        return Response({"data": data}, 200)
