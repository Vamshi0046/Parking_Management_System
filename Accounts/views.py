from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib import auth

from django.contrib import messages

def registerpage(request):
    if request.method == "POST":
        usernamee = request.POST['username']  
        # username is name in input tag
        passwordd = request.POST['password']
        confpasswordd = request.POST['confpassword']

        if passwordd == confpasswordd:
            if User.objects.filter(username=usernamee).exists():
                                   # 
                print("try another")
                return redirect('registerpage')
         
            else:
                user = User.objects.create_user(username=usernamee, password=passwordd)
                user.save()
                return redirect('loginpage')
        else:
            print('password didnt match ')
            return redirect('registerpage')
    else:
        return render(request, 'registerpage.html')
    


    
def login(request):
    if request.method=="POST":
        usernamee=request.POST['username']
        passwordd=request.POST['password']

        user = auth.authenticate(username=usernamee, password=passwordd)

        if user is not None:
            auth.login(request,user)
            print("Login is sucess")
            return redirect('dashboard')
        else:
            return redirect('loginpage')
    else:
        return render(request, 'loginpage.html')



def logout(request):
    if request.method=='POST':
        auth.logout(request)
        print('Loggedout from website')
        return redirect('loginpage')
    




def account_setting(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        reenter_password = request.POST['reenter_password']

        if not request.user.check_password(current_password):
            messages.error(request, 'Invalid current password.')
            return redirect('account_settings')

        if new_password != reenter_password:
            messages.error(request, 'New password and re-entered password do not match.')
            return redirect('account_settings')

        user = request.user
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password updated successfully.')
        return redirect('account_settings')

    return render(request, 'account_setting.html')
