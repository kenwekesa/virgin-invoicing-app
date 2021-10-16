
from accounts.models import Userlogin
from django.views.generic import CreateView

from django.contrib.auth.decorators import login_required

from django.shortcuts import  render, redirect



def login(request):
    return render(request, 'forms/loginpage.html')

@login_required
def home(request):
    #context = {'posts': Post.objects.all()}
    return render(request, 'index.html')#,context)




