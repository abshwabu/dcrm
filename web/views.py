from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,'Login successful')
            return redirect('home')
        else:
            messages.error(request,'Try again')
            return redirect('home')
    else:
        return render(request ,'home.html',{'records':records})
    
def logout_user(request):
    logout(request)
    messages.success(request,'Logout successful')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Register successful')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_records= Record.objects.get(id=pk)
        return render(request, 'record.html',{'customer_records':customer_records})
    else:
        messages.error(request,'Loin first')
        return render(request, 'home.html',{})
    
