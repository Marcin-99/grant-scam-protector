from django.urls import re_path
from .views import WhisperIntegrationView

urlpatterns = [
    re_path('whisper', WhisperIntegrationView.as_view(), name='open-ai-integration-whisper')
]
