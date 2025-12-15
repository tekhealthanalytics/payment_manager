from django.db import models

# Create your models here.
class PlanDetails(models.Model):
    source_website_plan=models.CharField(max_length=100)
    plan_name=models.CharField(max_length=50)
    amount=models.FloatField()
    def __str__(self):
        return self.source_website
    
class OrderIdDetails(models.Model):
    order_id=models.CharField(max_length=30,primary_key=True)
    plan=models.ForeignKey(PlanDetails,on_delete=models.CASCADE)
    cust_email=models.CharField(max_length=50)
    mobile_number=models.BigIntegerField(default=0000000000)
    cust_name=models.CharField(max_length=50,default="Unknown")
    def __str__(self):
        return self.order_id
    
class PaymentDetails(models.Model):
    payment_id=models.CharField(max_length=50,primary_key=True)
    order_details=models.ForeignKey(OrderIdDetails,on_delete=models.CASCADE)
    plan_details=models.ForeignKey(PlanDetails,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.payment_id
