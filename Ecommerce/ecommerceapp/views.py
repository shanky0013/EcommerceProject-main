from django.shortcuts import render,redirect
from .models import Contact,Product,Order,OrderUpdate
from . import secret_key
from django.views.generic import View
from django.contrib import messages
import math
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from paytmCheckSum import Checksum
# Create your views here.
MERCHANT_KEY=secret_key.MK

def index(request):
    total=[]
    categorised_products=Product.objects.values("category","id")
    categories={item['category'] for item in categorised_products}# dictionary of {categories}
    for category in categories:
        productList=Product.objects.filter(category=category)
        n=len(productList)
        pages=n//4+math.ceil((n/4)-(n//4))
        total.append([productList,range(1,pages),pages])

    context={"totalProducts":total}
    return render(request, "index.html",context)


def contact(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        desc=request.POST["desc"]
        phone_number=request.POST["phNo"]
        newContact=Contact(username=name,email=email,desc=desc,phone_number=phone_number)
        newContact.save()
        messages.info(request,"Thank you for your query")
        return render(request, "contact.html")
    return render(request, "contact.html")

class checkout(View):
    def get(self,request):
        if not request.user.is_authenticated:
            messages.warning("Login to check out")
            return redirect('/login');
        return render(request,"checkout.html")

    def post(self,request):
        if not request.user.is_authenticated:
            messages.warning("Login to check out")
            return redirect('/login');
        name=request.POST['name']
        email=request.POST['email']
        address1=request.POST['address1']
        address2=request.POST['address2']
        city=request.POST['city']
        state=request.POST['state']
        pin_code=request.POST['pin_code']
        phone_number=request.POST['phone']
        itemList=request.POST['itemsJson']
        totalAmount=request.POST['amt']

        order=Order(name=name,email=email,address1=address1,address2=address2,city=city,state=state,pin_code=pin_code,phone_number=phone_number,itemList=itemList,totalAmount=totalAmount)
        order.save()
        id=order.order_id
        updatedOrder=OrderUpdate(order_id=id,updated_desc="Order Has been Placed")
        updatedOrder.save()
        done=True
        #PAYTM INTEGRATION
        oid=str(id)+"shopiverseID"
        param_dict={
            'MID':secret_key.MID,
            'ORDER_ID':oid,
            'TXN_AMOUNT':str(totalAmount),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/'
        }
        param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'paytm.html',{'param_dict':param_dict})


def about(request):
    return render(request, "about.html")

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login and Try Again")
        return redirect('/login')
    currentUser=request.user.email
    items=Order.objects.filter(email=currentUser)
    for item in items:
        id_=item.oid
        rid=id_.replace("shopiverseID","")

    status=OrderUpdate.objects.filter(order_id=int(rid))

    return render(request,"profile.html",context={"items":items,"status":status})

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            orderID=response_dict['ORDERID']
            transactionAmount=response_dict['TXNAMOUNT']
            rid=orderID.replace("shopiverseID","")
            selectedOrders= Order.objects.filter(order_id=rid)
            print(selectedOrders)
            print(orderID,transactionAmount)
            for orders in selectedOrders:

                orders.oid=orderID
                orders.amountpaid=transactionAmount
                orders.paymentstatus="PAID"
                orders.save()
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})