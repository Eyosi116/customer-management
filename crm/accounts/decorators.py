from django.http import HttpResponse
from django.shortcuts import redirect

#This decorator will be used to restrict access to certain views based on whether the user is authenticated (logged in).
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
         # Check if the user is already authenticated (logged in)
         if request.user.is_authenticated:
        # If the user is authenticated, redirect them to the 'home' page
            return redirect('home')
         else:
            return view_func(request, *args, **kwargs)
         
    return wrapper_func

# This is a custom decorator that checks if a user belongs to specific roles to access a view.
# It takes a list of allowed roles as an argument.

def allowed_users(allowed_roles=[]):
    # The outer decorator function, which accepts the view function as its argument.
    def decorator(view_func):
        # The wrapper function, which is executed when the view is accessed.
        def wrapper_func(request, *args, **kwargs):
            
            # Initialize the 'group' variable as None.
            group = None

            # Check if the user belongs to any groups.
            if request.user.groups.exists():
                # If the user belongs to groups, get the name of the first group.
                group = request.user.groups.all()[0].name

            # Check if the user's group is in the list of allowed roles.
            if group in allowed_roles:
                # If the user's group is allowed, execute the original view function.
                return view_func(request, *args, **kwargs)
            else:
                # If the user's group is not allowed, return an HTTP response indicating unauthorized access.
                return HttpResponse('You are not authorized to view this page')

        # Return the wrapper function, which replaces the original view function.
        return wrapper_func

    # Return the decorator function, which can be applied to views using the @ syntax.
    return decorator



# This is a custom decorator called 'admin_only' designed to restrict access to views for specific user groups.

from django.http import HttpResponse
from django.shortcuts import redirect

# ...

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login')

    return wrapper_func
