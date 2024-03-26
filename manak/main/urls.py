from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("report", views.report, name="report"),
    path("report/guest", views.guest, name="guest"),
    path("admin-report", views.admin_report, name="admin_report"),
    path("admin-generate-pdf", views.admin_generate_pdf, name="admin_generate_pdf"),
    path("pdf/<str:file_name>/", views.send_pdf_response, name="pdf_response"),
    path("download-pdf", views.download_pdf, name="download_pdf"),
    path("update", views.update_report, name="update"),
    path("update_price", views.update_price, name="update_price"),
    path("remove_changes", views.remove_changes, name="remove_changes"),
    path("print", views.printf, name="print"),
    path("login", views.login, name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.register,name="register"),
    # path('terms/',views.terms,name="terms"),

]  

