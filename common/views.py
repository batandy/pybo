from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password

def signup(request):
    """
    회원가입
    """
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form=UserCreateForm()
    return render(request,'common/signup.html', {'form':form})


@login_required
def change_password(request):
    if request.method == "POST":
        user = request.user
        origin_password = request.POST["origin_password"]
        if check_password(origin_password, user.password):
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
                return redirect('common:profile_page')
            else:
                messages.error(request, "새 비밀번호가 일치하지 않습니다.")
                return render(request, 'common/change_password.html')
        else:
            messages.error(request, "현재 비밀번호가 일치하지 않습니다.")
            return render(request, 'common/change_password.html')
    else:
        return render(request, 'common/change_password.html')



# Create your views here.
@login_required(login_url='common:login')
def profile_index(request):
    return render(request, 'common/profile_page.html')
    
#네이버 지도
def map(request):
    return render(request, 'common/naver_map.html')