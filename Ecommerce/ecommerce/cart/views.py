from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart,Account,Order
# Create your views here.

@login_required
def add_to_cart(request,p):
    product=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=product,user=u)
        if(cart.quantity<cart.product.stock):
               cart.quantity+=1
        cart.save()
    except:
        cart=Cart.objects.create(product=product,user=u,quantity=1)
        cart.save()
    return redirect('cart:cartview')
def cartview(request):
    sum = 0
    u=request.user
    try:
       c=Cart.objects.filter(user=u)
       for i in c:
           sum += i.quantity * i.product.price

    except:
        pass
    return render(request,'cart.html',{'c':c,'total': sum})

def remove_from_cart(request,p):
    c=Product.objects.get(name=p)
    c.delete()
    return redirect('cart:cartview')

def decrement(request,p):
    product = Product.objects.get(name=p)
    u = request.user
    try:
        cart = Cart.objects.get(product=product, user=u)
        if(cart.quantity >1):
            cart.quantity = cart.quantity-1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return redirect('cart:cartview')
def orderform(request):
    if(request.method=='POST'):
        a=request.POST['a']
        p = request.POST['p']
        n= request.POST['n']
        u=request.user
        cart=Cart.objects.filter(user=u)
        total = 0
        for i in cart:
            total+=i.quantity*i.product.price#cartil ulla items total amount
        ac=Account.objects.get(acctnum=n)# accountno: n ayitulla personte complete details acil undi
        if(ac.ammount>=total):#acil ninni ammount eduti ati totalil ulla amount ayiti check cheyti
            ac.ammount=ac.ammount-total# enitti total amountil ninni cart items amount kurakkum
            ac.save()
            for i in cart:# create record in order table for each object in cart table for the current user
                o=Order.objects.create(user=u,product=i.product,address=a,phone=p,noofitem=i.quantity,order_status="paid")
                o.save()
                i.product.stock=i.product.stock-i.quantity
                i.product.save()
            cart.delete()# clear the cart items for the current user
            msg="order placed successfully"
            return render(request,'orderdetail.html',{'m':msg})
        else:
            msg="Insufficient amount in user account.You cannot place order."
            return render(request, 'orderdetail.html', {'m': msg})
    return render(request,'orderform.html')
def orderview(request):
    u = request.user
    c = Order.objects.filter(user=u)
    return render(request,'orderview.html',{'c':c})











