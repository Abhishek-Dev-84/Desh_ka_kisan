from django.shortcuts import render,redirect,get_object_or_404
from .models import MyUser, Contact , Product , Order
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from contact.backends import MyUserAuthBackend
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# from django.core.management import call_command
# from django.http import HttpResponse

# def run_migrations(request):
#     call_command('makemigrations', interactive= False)
#     call_command('migrate', interactive= False)
#     return HttpResponse("Migrations done!")

# Create your views here.
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('message')
        if email and text :
            user = Contact(name=name, email=email, message=text)
            user.save()
    return render( request , 'contact.html')

def index(request):
    return render(request,'index.html')

def help(request):
    return render(request,'help.html')

def features(request):
    return render(request,'features.html')

def signup(request):
    
    if request.method == 'POST':
        username = request.POST.get('user')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        choice = request.POST.get('options')
        if phone_no and password and  choice:
            user = MyUser.objects.create_user(username = username,phone_no = phone_no, password = password,choice = choice)
            user.save()
            if choice == 'Buyer':
                return redirect('/')
            else:
                return redirect('/')
        else:
            return render(request,'signup',{'error':'All fields are required.'})

    return render(request,'signup.html')
        

def buyer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.choice == 'Buyer':
                login(request,user)
                return redirect('buyer-dashboard/')
            else:
                messages.error(request,'Not a Buyer account')
        else:
            messages.error(request,'Invalid username or password')

    return render(request,'buyer-login.html')

def seller_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None and user.choice.lower() == 'seller':
            login(request,user)
            return redirect('seller-dashboard')
        elif user is not None:
            messages.error(request,'Not a seller account')
        else:
            print('Not a seller account!!')
            
    else:
        messages.error(request,'Invalid username or password or not a seller account')
    return render(request,'seller-login.html')


@login_required(login_url='buyer-login/')
def buyer_dashboard(request):
    Products = Product.objects.all()
    return render(request,'buyer-dashboard.html',{'products': Products})


@login_required(login_url='seller-login/')
def seller_dashboard(request):
    if request.user.choice.lower() !='seller':
        return redirect(request,'seller-login')
    return render(request,'seller-dashboard.html')


def Orders(request):
    if not request.user.is_authenticated:
        return redirect('buyer-login')
    orders = Order.objects.filter(buyer = request.user).order_by('-order_at')
    return render(request,'orders.html',{'orders':orders})


@never_cache
@login_required(login_url='buyer-login/')
def logout_buyer(request):
    logout(request)
    return render(request,'logout_buyer.html')


def manage_listings(request):
    products = Product.objects.filter(seller = request.user)
    return render(request,'manage-listings.html',{'products':products})


def order_list(request):
    orders = Order.objects.filter(Product__seller = request.user)
    return render(request,'order-list.html',{'orders': orders })


def profile_settings(request):
    return render(request,'profile-settings.html',{'user': request.user,})

@never_cache
def Logout(request):
    logout(request)
    return render(request,'logout.html')

# @never_cache
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':       
        order = Order(
            buyer=request.user,
            Product=product,
            quantity=int(request.POST.get('quantity', 1)),
            username=request.POST.get('username'),
            full_name=request.POST.get('fullname'),
            mobile=request.POST.get('mobile'),
            house=request.POST.get('house'),
            city=request.POST.get('city'),
            street=request.POST.get('street'),
            landmark=request.POST.get('landmark'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            status='pending',
        )        
        order.save()
        print("order saved:",order)
        return redirect('order_confirmed', order_id=order.id) 
    
    
    return render(request, 'buy_now.html', {'product': product})

def order_confirmed(request,order_id):
    order = Order.objects.get(id=order_id)
    product = order.Product

    context = {
        'order': order,
        'product':product
    }
    return render(request,'order_confirmed.html',context)

# @never_cache
def orders_list(request):
    if request.user.is_seller:
        orders = Order.objects.filter(Product__seller = request.user).order_by('-order_at')
    else:
        orders = Order.objects.filter(buyer = request.user).order_by('-order_at')
    return render(request,'orders.html',{'orders': orders})

# @never_cache
def add_product(request):
    if request.method == 'POST':
       name = request.POST.get('name')
       price = request.POST.get('price')
       quantity = request.POST.get('quantity')
       category = request.POST.get('category')
       unit = request.POST.get('unit')
       description = request.POST.get('description')
       image = request.FILES.get('image')
       print("DEBUG FORM VALUES:")
       print("product name:",{name})
       print("price:",{price})
       print("quantity:",{quantity})
       print("category:",{category})
       print("Unit:",{unit})
       print("description:",{description})
       print("image:",{image})
       print("user:",{request.user})
       if name and price and quantity and category and description and image: 
            product = Product(seller = request.user,
                              name = name,
                              price = price,
                              quantity = quantity,
                              category = category,
                              description = description,
                              unit = unit , 
                              image = image)
            product.save()
            return redirect('seller-dashboard')
       else:
            error = "please fill all fields correctly."
            return render(request,'add-product.html',{'error':error})
    return render(request,'add-product.html')
    
    def track_order(request,order_id):
        order = get_object_or_404(Order,id='order_id',buyer = request.user)
        return render(request,'orders.html',{'order':order})
    
def delete_product(request,product_id):
    product = get_object_or_404(Product,id=product_id,seller = request.user)
    product.delete()
    return redirect('manage-listings')

def update_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user.username = username
        user.phone_no = phone

        if password:
            user.set_password(password)
        update_session_auth_hash(request,user)
        user.save()
        messages.success(request,'profile updated successfully.')
        return redirect('seller-dashboard')
    else:
        return render(request,'profile-settings.html',{'user': request.user,})
    return render(request,'profile-settings.html',{'user': request.user,})
