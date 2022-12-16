from django.urls import re_path
from .views import WhisperIntegrationView, AlertsView

urlpatterns = [
    re_path('whisper', WhisperIntegrationView.as_view(), name='open-ai-integration-whisper'),
    re_path('alerts', AlertsView.as_view(), name='open-ai-integration-alerts')
]
