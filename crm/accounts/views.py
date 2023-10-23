from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import CreateUserForm, OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


from django.contrib.auth.decorators import login_required

# ...

@unauthenticated_user
def register(request):
    
    if request.method == 'POST':
        #Inside the POST block, a new instance of the CreateUserForm
        # is created, this time populated with the data submitted in the POST request. This allows the view to work with the form data submitted by the user.
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #it extracts the username of the newly created user from the form's cleaned data.
            username = form.cleaned_data.get('username')
            # Retrieve the 'customer' group from the database based on its name
            group = Group.objects.get(name = 'customer')
            # Add the user to the 'customer' group
            user.groups.add(group)
            #messaging framework is used here to display a success message to the user
            messages.success(request, 'Account created successfully for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

  
    
    # If the user is not authenticated (not logged in) and the request method is POST
    if request.method == 'POST':
        
        # Get the 'username' and 'password' from the POST data submitted by the user
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user with the provided 'username' and 'password'
        user = authenticate(request, username=username, password=password)

        # Check if the user authentication was successful
        if user is not None:
            # If authentication was successful, log in the user
            login(request, user)
            # Redirect the user to the 'home' page
            return redirect('home')
        else:
            # If authentication failed, display an error message to the user
            messages.info(request, 'Username OR Password is incorrect!')

    # Create an empty context dictionary
    context = {}
    # Render the 'login.html' template with the context data
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    context = {'orders': orders}
    return render(request, 'accounts/user.html', context)



@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count
    pending = orders.filter(status='Pending').count
    context = {'orders': orders, 'customers': customers, 'delivered': delivered, 'pending': pending, 'total_orders': total_orders}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()##returns all orders tha have been made by the coustomer above(using it's ID)
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'customer': customer, 'order_count': order_count, 'myFilter': myFilter} 
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=10) 
    customer = Customer.objects.get(pk=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance = customer)
    

    #form = OrderForm(initial = {'customer': customer} )

    if request.method == 'POST':
        #print('printing post', request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context = {'form': form}

    if request.method == 'POST':
        #print('printing post', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    context = {'item': order}

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', context)


