from django.shortcuts import render, get_object_or_404
from orders.models import Order
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    "payment/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime


def ecpay_main(order_id):
    order = get_object_or_404(Order, id=order_id)
    price = order.get_total_cost()

    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': price,
        'TradeDesc': '訂單測試',
        'ItemName': str(order.id),
        'ReturnURL': 'https://hsveg-django.herokuapp.com/payment/end_return/', # 顧客填完付款資料送出後的頁面
        'ChoosePayment': 'ALL',
        'ClientBackURL': 'https://hsveg-django.herokuapp.com/payment/end_page/',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://hsveg-django.herokuapp.com/payment/end_page',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

    extend_params_1 = {
        'ExpireDate': 7,
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
        'ClientRedirectURL': '',
    }

    extend_params_2 = {
        'StoreExpireDate': 15,
        'Desc_1': '',
        'Desc_2': '',
        'Desc_3': '',
        'Desc_4': '',
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
        'ClientRedirectURL': '',
    }

    extend_params_3 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_4 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }

    inv_params = {
        # 特店自訂編號
        # 'RelateNumber': 'Xxx0001',
        # 客戶編號
        # 'CustomID': 'Xxx_0000001',
        # 統一編酪
        # 'CustomerIdentifier': '12345678',
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 客戶手機號碼
        # 'CustomerPhone': '0912345678',
        # 客戶電子郵件
        # 'CustomerEmail': 'user@example.com',
        # 通關方式
        # 'ClearanceMark': '2',
        # 課稅類別
        # 'TaxType': '1',
        # 載具類別
        # 'CarruerType': '',
        # 捐贈註記
        # 'Donation': '',
        # 捐贈碼
        # 'LoveCode': '168001',
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 延遲天數
        # 'DelayDay': '0',
        # 字軌類別
        # 'InvType': '07',
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='3002607',
        HashKey='pwFHCqoQZGmho4w6',
        HashIV='EkRm7iFT261dpevs',
    )

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    order_params.update(extend_params_3)
    order_params.update(extend_params_4)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
        print('##############')
        print(final_order_params)
        print('##############')
        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5' # 測試環境
        # action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        return html # print(html)
    except Exception as error:
        print('An exception happened: ' + str(error))





