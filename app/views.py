from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from app.forms import *
from django.core. mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            send_mail('Registration Form',
            'Thank you for registering your mail successfully..',
            'gsandeep0002@gmail.com',
            [MUFDO.email],
            fail_silently=True
            )

            return HttpResponse('Registration done successfully...')
        else:
            return HttpResponse('Invalid data....')

    return render(request,'registration.html',d)



def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')
    

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username 
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'user_login.html')
        



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        # return HttpResponse('Password Changed Sucessfully..')
        return HttpResponseRedirect(reverse('user_login'))

    return render(request,'change_password.html')




def forgot_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('Reset password is done successfully...')
            # return HttpResponseRedirect(reverse('user_login'))
        else:
            return HttpResponse('User name not found in database')

    return render(request,'forgot_password.html')








# rvof ldsr vopj yqve