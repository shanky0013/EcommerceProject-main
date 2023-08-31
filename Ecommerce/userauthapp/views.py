from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import generate_token
from django.views.generic import View
from django.utils.encoding import force_bytes,force_str
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
import time
# Create your views here.
def signup(request):
    if(request.method=="POST"):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if(password!=confirm_password):
            messages.warning(request,"password is not matching")
            return render(request,"signup.html")
        
        try:

            if(User.objects.get(email=email)):
                messages.info(request,"This account already exists.")
                return render(request,"signup.html")
                # return HttpResponse("Email already exists")
        except Exception as e:
            print(e)
        user=User.objects.create_user(username,email,password)
        user.is_active=False
        # t=time.time()
        user.save()
        email_subject="Acount Activation Link"
        message=render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        try:
            email_message.send()
        except Exception as e:
            print(e)
            messages.warning(request,e)
            user.delete()
            return render(request,"signup.html")
        messages.success(request,"Acount Activation Link Has been Sent. Check your gmail")
        return redirect('/auth/login')
    return render(request,"signup.html")

class ActivateAccount(View):
    def get(self,request,uidb64,token):
        try:
            #uid is the primary key as I am decoding the encoded primary key
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as e:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account Created Successfuly. Happy Shopping")
            return redirect('/auth/login/')
        return render(request,'activationFailed.html')




def handlelogin(request):
    if(request.method=="POST"):
        username=request.POST['username']
        password=request.POST['pass1']
        email=request.POST['email']
        loggedUser=authenticate(username=username,email=email,password=password)

        if loggedUser is not None:
            login(request,loggedUser)
            messages.success(request,"Logged In successfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auth/login/')
    
    return render(request,"login.html")

def handlelogout(request):
    logout(request)
    messages.success(request,"Logged Out Sucessfully")
    return redirect('/auth/login')


