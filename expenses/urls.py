from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ExpenseViewSet,
    RegisterView,
    ExpenseSummaryView
)

router = DefaultRouter()

router.register(
    'expenses',
    ExpenseViewSet,
    basename='expense'
)

urlpatterns = [
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    path(
        'summary/',
        ExpenseSummaryView.as_view(),
        name='summary'
    ),
]

urlpatterns += router.urls