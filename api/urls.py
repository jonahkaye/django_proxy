from django.urls import path
from .views import InferenceProxyView, RegisterView


urlpatterns = [
	path('inference_proxy/', InferenceProxyView.as_view(), name='inference_proxy'),
    path('register/', RegisterView.as_view(), name='register'),
]
