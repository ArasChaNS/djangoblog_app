from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from  django.contrib.auth.models import User
from  django.contrib.auth import login,authenticate,logout
from django.middleware.csrf import CsrfViewMiddleware




class CustomCsrfMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        raise CustomCsrfMiddleware("Zaten Giriş Yapıldı veya Bir Hata Var...")
        # You can do things here before the error is raised.


        return super(CustomCsrfMiddleware, self).process_view(request, callback, callback_args, callback_kwargs)
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username =  form.cleaned_data.get("username")
            password =  form.cleaned_data.get("password")
            

            newUser = User(username = username)
            newUser.set_password(password)

            context = {
            "form" : form,
                    }
            if User.objects.filter(username = username).first():
                messages.warning(request, "Bu İsim Daha Önce Alındı...")
                return render(request,"register.html",context)

            newUser.save()
            messages.success(request,"Başarıyla Kayıt Oldunuz...")
            login(request,newUser)

            return redirect("index")
        context = {
            "form" : form,
        }
        return render(request,"register.html",context)
    else:
        form = RegisterForm
        context = {
            "form" : form,
        }
        return render(request,"register.html",context)
    """
    form = RegisterForm()
    context = {
        "form" : form,
    }
    return render(request,"register.html",context)

    """

def loginUser(request):
    form = LoginForm(request.POST or None)
    
    context = {
        "form" : form,
    }
    
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı...")
            return render(request,"login.html",context)
        
        messages.success(request,"Başarıyla Giriş Yaptınız...")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect("index")