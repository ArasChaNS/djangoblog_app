from django.contrib import admin
from django.urls import path
from article.views import index
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "user"


urlpatterns = [
    path('register/',views.register,name = "register"),
    path('login/',views.loginUser,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)