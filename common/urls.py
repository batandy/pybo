from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views

app_name='common'

urlpatterns=[
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    #pofile
    path('profile/', views.profile_index, name='profile_page'),
    path('profile/change_password/<int:user_id>', views.change_password, name='change_password'),

    #map
    path('map/', views.map, name='naver_map'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)