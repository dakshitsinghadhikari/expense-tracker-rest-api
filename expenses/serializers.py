from rest_framework import serializers
from .models import Expense
from django.contrib.auth.models import User
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        Fields = [
            'id',
            'user',
            'amount',
            'month',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
        ]



class ExpenseSerializer(serializers.ModelSerializer):
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        else:
            return value
    def validate_title(self,value):
        if not value:
            raise serializers.ValidationError("title cannot be empty")
        else:
            return value
    def validate_category(self,value):
        if not value:
            raise serializers.ValidationError("category cannot be empty")
        else: return value
    class Meta:
        model = Expense
        fields = [
            'id',
            'user',
            'title',
            'amount',
            'category',
            'description',
            'date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
            'updated_at',
        ]




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
