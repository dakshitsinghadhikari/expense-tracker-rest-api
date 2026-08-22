from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .models import Expense
from .serializers import ExpenseSerializer, RegisterSerializer
from django.db.models import Sum, Avg


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['amount', 'date', 'title']
    ordering = ['-date']

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)

        category = self.request.query_params.get('category')
        date = self.request.query_params.get('date')
        search = self.request.query_params.get('search')
        start_date=self.request.query_params.get('start_date')
        end_date=self.request.query_params.get('end_date')

        if category:
            queryset = queryset.filter(category__iexact=category)

        if date:
            queryset = queryset.filter(date=date)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if start_date:
            queryset = queryset.filter(
                date__gte = start_date
            )
        if end_date:
            queryset = queryset.filter(
                date__lte=end_date
            )


        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ExpenseSummaryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)

        total_expenses = expenses.aggregate(
            total=Sum('amount')
        )['total'] or 0

        average_expense = expenses.aggregate(
            average=Avg('amount')
        )['average'] or 0

        number_of_expenses = expenses.count()

        category_totals = {}

        for category in expenses.values_list(
                'category',
                flat=True
        ).distinct():
            category_total = expenses.filter(
                category=category
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

            category_totals[category] = category_total

        return Response({
            'total_expenses': total_expenses,
            'number_of_expenses': number_of_expenses,
            'average_expense': average_expense,
            'category_totals': category_totals,
        })
