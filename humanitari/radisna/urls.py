from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path("", views.index, name="index"),
                  path("register", views.register, name="register"),
                  path("login", views.login_view, name="login"),
                  path("logout", views.logout_view, name="logout"),
                  path("helpme", views.helpme, name="helpme"),
                  path("check", views.check, name="check"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
