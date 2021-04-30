from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('',views.home, name="home"),
    path('login/',views.login, name="login"),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('profile/',views.profile, name="profile"),
    path('addInstitute/',views.addInstitute, name="addInstitute"),
    path('allUser/',views.allUser, name="allUser"),
    path('addFaculty/',views.addFaculty, name="addFaculty"),
    path('logout/',views.logout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)