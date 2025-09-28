from rest_framework import serializers
from .models import Customer, Loan

class CustomSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
        
class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length = 100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    monthly_income = serializers.IntegerField()
    phone_number = serializers.IntegerField()

    def create(self, validated_data):
        approved_limit = round((36 * validated_data["monthly_income"]/100000)) * 100000
        customer = Customer.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            age=validated_data["age"],
            monthly_income=validated_data["monthly_income"],
            approved_limit=approved_limit,
            phone_number=validated_data["phone_number"]
        )
        return customer

class ProcessLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()

class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "phone_number", "age"]

class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer()

    class Meta:
        model = Loan
        fields = [
            "id",
            "customer",
            "loan_amount",
            "interest_rate",
            "monthly_installment",
            "tenure"
        ]

class LoanListSerializer(serializers.ModelSerializer):
    repayments_left = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "id",
            "loan_amount",
            "interest_rate",
            "monthly_installment",
            "repayments_left"
        ]

    def get_repayments_left(self, obj):
        return max(0, obj.tenure - obj.emis_paid_on_time)