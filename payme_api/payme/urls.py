from django.urls import path

from payme.views import MerchantAPIView, SuccessNotifier

urlpatterns = [
    path('merchant', MerchantAPIView.as_view()),
    path('success', SuccessNotifier.as_view())

]
