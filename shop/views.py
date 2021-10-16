from django.shortcuts import render, redirect
from .models import Product, Contact, Order, OrderUpdate, Customer
from math import ceil
import json
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
from django.http import HttpResponse, response


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        messages.success(request, 'Thanks for contacting us. We will get back to you soon!')

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        email = request.COOKIES['email']

        customer = Customer.objects.filter(email=email)
        if len(customer) > 0:
            #return render(request, 'shop/checkout.html', params)
            name = customer[0].firstName + ' ' + customer[0].lastName
            
            order = Order(items_json=items_json, name=name, email=email, address=customer[0].address, state=customer[0].state, 
                    zip_code=customer[0].zip, phone=customer[0].phone)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
            update.save()
            
            thank = True
            id = order.order_id
            #messages.success(request, 'Your order has been successfully placed! Use order id ' + str(id) + ' to track your order.')
            #return redirect('/shop/')
            return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    else:
        try:
            userName = request.COOKIES['userName']
            email = request.COOKIES['email']
            print(email)
            print(userName)

            customer = Customer.objects.filter(email=email)
            if len(customer) > 0:
                address = customer[0].address + ', '+ customer[0].state + ', ' + customer[0].zip
                name = customer[0].firstName + ' ' + customer[0].lastName
                params = {'address': address, 'phone': customer[0].phone, 'name': name, 'email': email}
                print(params)
                return render(request, 'shop/checkout.html', params)
            
        except Exception as e:
            print(e)
            messages.info(request, 'Please sign-in first!')
            return redirect('/shop/signin')

        
def signin(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print(email)
        #print(password)
        user = Customer.objects.filter(email=email, password=password)
        if len(user) > 0:
            print(user[0].firstName)
            messages.success(request, 'Sign-in successful!')
            response = redirect("/shop/")
            response.set_cookie('userName', user[0].firstName)
            response.set_cookie('email', user[0].email)
            
            return response
    
        else:
            messages.warning(request, 'Please enter correct email and password!')
            return render(request, 'shop/signin.html')
    else:
        return render(request, 'shop/signin.html')
    
def signout(request):
    return render(request, 'shop/signout.html')


def signup(request):
    if request.method=="POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        password = request.POST.get('password1')
        
        customer = Customer.objects.filter(email=email)
        if len(customer) > 0:
            messages.info(request, 'One sweettooth account already exists with this email ID! Try creating using another one!')
            return redirect("/shop/signup")
    
        else:
            customer = Customer(firstName=firstName, lastName=lastName, email=email, phone=phone, address=address, state=state, zip=zip, password=password)
            customer.save()
            messages.success(request, 'Account created successfully! Please proceed to sign-in!')
            return redirect("/shop/signin")
    else:
        return render(request, 'shop/signup.html')

def temp(request):
    return render(request, 'shop/temp.html')

def temp2(request):
    return render(request, 'shop/temp2.html')

def account(request):
    if request.method == "POST":
        email = request.COOKIES['email']
        customer = Customer.objects.filter(email=email)[0]
        phone = customer.phone
        address = customer.address
        state = customer.state
        zip = customer.zip
        password = customer.password
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        customer.state = request.POST.get('state')
        customer.zip = request.POST.get('zip')
        customer.password = request.POST.get('password2')
        
        if(phone != customer.phone or address != customer.address or state != customer.state or zip != customer.zip or password != customer.password):
            messages.success(request, 'Your account details have been updated!')
            customer.save()
            return redirect('/shop/')
        else:
            return redirect('/shop/')
        
    else:
        email = request.COOKIES['email']
        customer = Customer.objects.filter(email=email)
        if len(customer) > 0:
            address = customer[0].address.replace(" ","")
            #print(address)
            params = {'address': address, 'phone': customer[0].phone, 'firstName': customer[0].firstName, 'lastName': customer[0].lastName, 'email': email, 'zip': customer[0].zip, 'state': customer[0].state, 'password': customer[0].password}      
            return render(request, 'shop/account.html', params)