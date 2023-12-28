from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
import razorpay
from .models import product,cart,customer,Payment,orderplaced,Wishlist
from .forms import customerprofileForm,CustomerRegistrationForm,customer
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
# Create your views here.
def homepage(request):
    return render(request,"app/home.html")

def about(request):
    return render(request,"app/about.html")


def contact(request):
    return render(request,"app/contact.html")

class categoryView(View):
    def get(self,request,val):
        Product=product.objects.filter(category=val)
        title= product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class categorytitle(View):
    def get(self,request,val):
        Product=product.objects.filter(title=val)
        title= product.objects.filter(category=Product[0].category).values('title')
        return render(request,"app/category.html",locals())
    

class productDetail(View):
    def get(self,request,pk):
        Product=product.objects.get(pk=pk)
        wishlist= Wishlist.objects.filter(Q(Product=Product)& Q(user=request.user))
        return render(request,'app/productdetails.html',locals())
    

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/CustomerRegistration.html',locals()) 
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations !User Regrister Success")
        
        else:
            messages.warning(request,"Invalid Input Date")
        return render(request,'app/CustomerRegistration.html',locals()) 
    
class profileView(View):
    def get(self,request):
        form=customerprofileForm()
        return render(request, 'app/profile.html',locals()) 
    def post(self,request):
        form = customerprofileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city=  form.cleaned_data['city']
            mobile= form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg= customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"congratulations ! profile save successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals()) 
    
def  address(request):
    add = customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add=customer.objects.get(pk=pk)
        form=customerprofileForm(instance=add)
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form =  customerprofileForm(request.POST)
        if form.is_valid():
            add = customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city=  form.cleaned_data['city']
            add.mobile= form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"congratulations ! profile save successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    Product=product.objects.get(id=product_id)
    cart(user=user,Product=Product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    Cart=cart.objects.filter(user=user)
    amount=0
    for p in Cart:
        value=p.quantity*p.Product.discount_price
        amount=amount+value
    totalamount= amount+40

    return render(request,'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add = customer.objects.filter(user=user)
        cart_item=cart.objects.filter(user=user)
        famount=0
        for p in cart_item:
            value=p.quantity*p.Product.discount_price
            famount=famount+value
            totalamount= famount+40
            razoramount=int(totalamount*100)
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
            data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_11" }
            payment_response = client.order.create(data=data)
            print(payment_response)
            #{'id': 'order_MZPpfknwlt77VS', 'entity': 'order', 'amount': 20500, 'amount_paid': 0, 'amount_due': 20500, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1694083183}
            order_id=payment_response['id']
            order_status=payment_response['status']
            if order_status == 'created':
                payment=Payment(
                    user=user,
                    amount=totalamount,
                    razorpay_order_id=order_id,
                    razorpay_payment_status=order_status

                )
                payment.save()

            return render(request,'app/checkout.html',locals())
        
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user=request.user
    Customer = customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    Cart=cart.objects.filter(user=user)
    for c in Cart:
        orderplaced(user=user,Customer=Customer,Product=c.Product,quantity=c.quantity,payment=payment).save()
        c.delete
    return redirect("orders")
def orders(request):
    Order_placed=orderplaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())

def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        C=cart.objects.filter(Q(Product=prod_id) & Q(user=request.user))
        for i in C:
            i.quantity+=1
            i.save()
        user=request.user
        Cart=cart.objects.filter(user=user)
        amount=0
        for p in Cart:
            value=p.quantity*p.Product.discount_price
            amount=amount+value
            totalamount= amount+40
        data={
            'quantity':i.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        C=cart.objects.filter(Q(Product=prod_id) & Q(user=request.user))
        for i in C:
            i.quantity-=1
            i.save()
        user=request.user
        Cart=cart.objects.filter(user=user)
        amount=0
        for p in Cart:
            value=p.quantity*p.Product.discount_price
            amount=amount+value
            totalamount= amount+40
        data={
            'quantity':i.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        C=cart.objects.filter(Q(Product=prod_id) & Q(user=request.user))
        C.delete()
        user=request.user
        Cart=cart.objects.filter(user=user)
        amount=0
        for p in Cart:
            value=p.quantity*p.Product.discount_price
            amount=amount+value
            totalamount= amount+40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def plus_wishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        Product=product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,Product=Product).save()
        data={
            'message':'Wishlist Added Successfully'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        Product=product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,Product=Product).delete()
        data={
            'message':'Wishlist Removed Successfully'
        }
        return JsonResponse(data)
