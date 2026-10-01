from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ExpenseViewSet,
    RegisterView,
    ExpenseSummaryView,
    BudgetViewSet
)

router = DefaultRouter()

router.register(
    'expenses',
    ExpenseViewSet,
    basename='expense'
)
router.register(
    'budgets',
    BudgetViewSet,
    basename='budget'
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
    path(
        'token/',
        obtain_auth_token,
        name='token'

    ),
]

urlpatterns += router.urls