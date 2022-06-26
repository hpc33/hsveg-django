from decimal import Decimal
from itertools import product
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse

# Create your views here.
from orders.models import Order
from .ecpay import ecpay_main
from django.http import HttpResponseRedirect
from datetime import datetime


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'TWD',
        # 'notify_url': 'http://{}{}'.format(host,
        #                                    reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'payment/process.html', {'order': order, 'form': form})
    

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


@csrf_exempt
def ecpay(request):
    order_id = request.session.get('order_id')
    return HttpResponse(ecpay_main(order_id))


def successful_payment(request):
    return render(request, 'payment/successful.html')


def failure_payment(request):
    return render(request, 'payment/fail.html')


@csrf_exempt
def end_page(request):
    print('to user server')
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('payment:fail'))
    
    if request.method == 'POST':
        result = request.POST.get('RtnMsg')
        print(result)
        if result == 'Successed':
            print('#######')
            print(request.POST.get('TradeNo'))
            print(request.POST.get('TradeAmt'))
            print(request.POST.get('TradeDate'))
            check = request.POST.get('CheckMacValue')
            print(check)
            print('#######')
            return HttpResponseRedirect(reverse('payment:success'))
        else:
            return HttpResponseRedirect(reverse('payment:fail'))


def end_return(request):
    if request.method == 'POST':
        return '1|OK'
