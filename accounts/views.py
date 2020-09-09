from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from contacts.models import Contact

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now Logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        # Get from Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        # Check if Passwords Match
        if password1 == password2:
            # Check if username exist
            if User.objects.filter(username=username).exists():
                messages.error(request, "That Username Is Already Registered!")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "That Email Is Already Used!")
                    return redirect('register')
                else:
                    # Now Register this User
                    user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'You are registered Successfuly, Now you can Login!')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords Do Not Match')
            return redirect('register')
        return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are now logged out.')
        return redirect('index')
    else:
        return redirect('login')


def dashboard(request):
    contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': contacts
    }
    return render(request, 'accounts/dashboard.html', context)
