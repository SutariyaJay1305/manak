from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("report", views.report, name="report"),
    path("admin-report", views.admin_report, name="admin_report"),
    path("update", views.update_report, name="update"),
    path("update_price", views.update_price, name="update_price"),
    path("remove_changes", views.remove_changes, name="remove_changes"),
    path("print", views.print, name="print"),
    path("login", views.login, name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.register,name="register"),

]  