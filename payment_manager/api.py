from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse,JsonResponse
from django.template.response import TemplateResponse
from .models import PaymentDetails, PlanDetails,OrderIdDetails
import razorpay

client = razorpay.Client(auth=("rzp_test_RmS9j2gPUxb05Y", "51Uh6aITDjgkce4ufp74fNY0"))

@api_view(['GET'])
def check_connection(request):
    return HttpResponse('server is live!!')


@api_view(['POST'])
def initiate_payment(request):
    data=request.data
    try:
        source_website=request.headers.get("Origin")
        if(source_website):
            print(f'source web : {source_website}')
        else:
            print('source website not found')
    
        # source_website=data['source_website']
        cust_email=data['customer_email']
        plan=data['plan_name']
        objs = PlanDetails.objects.filter(plan_name=plan)
        obj=None
        for p in objs:
            if p.source_website.lower() in source_website.lower():
                obj = p
                break
        # obj=PlanDetails.objects.filter(plan_name=plan).first()
        if obj:
            print(obj.id)
            order_id=generate_order_id(plan=obj,cust_email=cust_email,amount=obj.amount)
            if order_id:
                return TemplateResponse(
                     request,
                        "select_payment.html",
                         {"order_id": order_id,"amount":obj.amount}
                    )
        else:
            return HttpResponse("plan not found")
    except:
        return HttpResponse("incomplete information")

    



def generate_order_id(plan,cust_email,amount):
    try:
        data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data) # Amount is in currency subunits.
        order=OrderIdDetails.objects.create(
            order_id=payment['id'],
            plan=plan,
            cust_email=cust_email
        )
        print(order)
        return payment['id']
    except Exception as e:
        print(e)

@api_view(['POST'])
def payment_id(request):
    try:
        data =request.data
        print(data['razorpay_payment_id'])
        print(data['razorpay_order_id'])
        print(data['razorpay_signature'])
        order_id=data['razorpay_order_id']
        payment_id=data['razorpay_payment_id']

        order_details=OrderIdDetails.objects.filter(order_id=order_id).first()
        plan_details=order_details.plan

        payment=PaymentDetails.objects.create(
            payment_id=payment_id,
            order_details=order_details,
            plan_details=plan_details
        )

        print(payment)

        return HttpResponse('payment successful')
    except Exception as e:
        print('api call error')
        print(e)