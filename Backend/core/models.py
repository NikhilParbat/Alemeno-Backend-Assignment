from django.utils import timezone
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.BigIntegerField()
    monthly_income = models.BigIntegerField()
    approved_limit = models.BigIntegerField()
    phone_number = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Loan(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="loans"
    )
    loan_amount = models.BigIntegerField()
    tenure = models.IntegerField(help_text="Tenure in months")
    interest_rate = models.DecimalField(max_digits=6, decimal_places=3)  # annual %
    monthly_installment = models.BigIntegerField()
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} for Customer {self.customer.customer_id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)