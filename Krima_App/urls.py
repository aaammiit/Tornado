"""
URL configuration for a1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v.Page),
    path('home',v.home),
    path('delete_file/<int:id>',v.Delete),
    path('view_file/<int:id>',v.view_file),
    path('make_pm',v.Make_pm),
    path('pm_login',v.Pm_login),
    path('pm_home',v.Pm_home),
    path('push_to_pm/<int:id>',v.Push_PM_file),
    path('pm_view_file/<int:id>',v.Pm_view_file),
    path('verify_otp1',v.verify_otp1),
    path('logout_user',v.Logout_user),
    path('make_qc',v.Make_qc),
    path('qc_login',v.Qc_login),
    path('verify_otp2',v.verify_otp2),
    path('qc_home',v.Qc_home),
    path('push/<int:id>',v.Push_file),
    # path('delete_file1/<int:id>',v.Delete1),
    path('qc_view_file/<int:id>',v.Qc_view),
    path('filter_srh/<int:id>',v.Filter_srh),
    path('data_srh/<int:id>',v.Data_save),
    path('qc_edit_data/<int:id>/<int:pid>',v.Edit_data),
    path('Add_rows/<int:id>/<int:pid>',v.Add_rows),
    path('qc_filter_edit_data/<int:id>/<int:pid>',v.Qc_filter_edit),
    path('fil_Add_rows/<int:id>/<int:pid>',v.fil_Add_rows),
    path('qc_push/<int:id>',v.Qc_push),


    path('make_ed',v.Make_ed),
    path('ed_login',v.Ed_login),
    path('ed_home',v.Ed_home),
    path('verify_otp',v.verify_otp),

    path('ed_view_file/<int:id>',v.Ed_view_file),
    path('ed_filter_srh/<int:id>',v.Ed_Filter_srh),
    path('ed_data_srh/<int:id>',v.Ed_Data_save),
    path('ed_edit_data/<int:id>/<int:pid>',v.Ed_Edit_data),
    path('ed_filter_edit_data/<int:id>/<int:pid>',v.Ed_filter_edit),
    path('ed_push/<int:id>',v.Ed_push),

    path('qc_file_record',v.Qc_send_file_record),
    path('ed_file_record',v.Ed_send_file_record),
    path('Download/<int:id>',v.Download_file),
    path('about_us',v.About_us),
    path('all_user',v.All_user),
    # path('feature',v.Feautre),

]
