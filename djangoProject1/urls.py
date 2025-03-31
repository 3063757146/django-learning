"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app01 import views #引入views
urlpatterns = [
    # path("admin/", admin.site.urls),
    #   前端网址      前端对应执行函数
    path("depart/list/",views.depart_list),
    path("depart/add/",views.depart_add),
    path("depart/delete/",views.depart_delete),
    path("depart/<int:nid>/edit/",views.depart_edit),
#         要穿的id不放在?nid=xx了 改为放在url内部 更加安全
    path("users/list/",views.users_list),
    path("users/add/",views.users_add),
    path("users/<int:nid>/edit/", views.users_edit),
    path("users/<int:nid>/delete/", views.users_delete),

    path("mobile/list/",views.mobile_list),
    path("mobile/add/",views.mobile_add),
    path("mobile/<int:nid>/delete/", views.mobile_delete),
    path("mobile/<int:nid>/edit/", views.mobile_edit),

]
