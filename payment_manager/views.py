from django.shortcuts import render


def select_payment_page(request):
    return render(request, "select_payment.html")