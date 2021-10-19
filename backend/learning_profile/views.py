from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()
# Create your views here.


def register(request):
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('profile:login')
    context = {'form': form}
    return render(request, 'registration/register.html', context)
