from django.shortcuts import render, redirect
from .forms import CustomUserCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
# Create your views here.


@login_required(login_url='login')
def home_page(request):
	return render(request, 'home.html')

def login_page(request):
	
	page = 'login'
    
	if request.method == 'POST':
	    user = authenticate(
	        email = request.POST['email'],
	        password = request.POST['password']
	    )
	    if user is not None:
	        login(request, user)
	        return redirect('home')

	return render(request, 'login_register.html', {'page':page})

def logout_page(request):
    logout(request)
    return redirect('login')

def register_page(request):
	page = 'register'
	form = CustomUserCreateForm()
	if request.method == 'POST':
	    form = CustomUserCreateForm(request.POST)
	    if form.is_valid():
	        # Check if the email already exists
	        email = form.cleaned_data['email']
	        if User.objects.filter(email=email).exists():
	            # Display an error message or redirect as needed
	            return render(request, 'login_register.html', {'message': 'Email already exists.'})
	        # If email is unique, save the user
	        form.save()
	        # Redirect to a success page or login page
	        return redirect('login')
	return render(request, 'login_register.html', {'page':page, 'form':form})

@login_required(login_url='login')
def csrf_attack(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')

    if 'csrfmiddlewaretoken' not in request.POST:
        return render(request, 'home.html', {'error': 'CSRF token missing'})

    if request.POST['csrfmiddlewaretoken'] != \
            self.client.get_csrf_token():
        return render(request, 'home.html', {'error': 'CSRF token invalid'})

    return HttpResponseForbidden(
        content='CSRF attack detected',
    )

