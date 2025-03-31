from django.shortcuts import render,HttpResponse,redirect
from flask import request
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01 import models


def depart_list(request):
    queryset=models.Department.objects.all()
    return render(request,"depart_list.html",{"queryset":queryset})

def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户POST提交过来的数据（title输入为空）
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")

def depart_delete(request):
    nid=request.GET.get("nid")
    print(nid)
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request,nid):
    if request.method == "GET":
        obj=models.Department.objects.get(id=nid)
        return render(request,"depart_edit.html",{"obj":obj})
    newTitle=request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=newTitle)
    return redirect("/depart/list/")

def users_list(request):
    queryset=models.UserInfo.objects.all()
    # for obj in queryset:
    #     print(obj.id,obj.name,obj.password,obj.account)
    #     print(obj.create_time.strftime("%Y-%m-%d"))#时间处理
    #     print(obj.department.title)#数据库里存的是department_id, django封装外键 直接.获取那一整id行信息
    #     print(obj.get_gender_display())#.gender是数字  此封装函数直接获取元组汉字
    return render(request, "users_list.html", {"queryset":queryset})


from django import forms

class UserModelForm(forms.ModelForm):
    # 可在这写校验规则
    password = forms.CharField(min_length=6,label="密码",widget=forms.PasswordInput)

    class Meta:
        model = models.UserInfo
        #先填充user类   fields填写输入框需要的user字段
        fields = ["name","password","age","account","create_time","gender","department"]

# 给输入框加样式
# 法一  需要逐个加  麻烦
#         widgets={"name":forms.TextInput(attrs={"class":"form-control"}),
#                  "password":forms.PasswordInput(attrs={"class":"form-control"}),
#                  }

# 法二
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name,field in self.fields.items():
            # if name=="password":
            #     continue  也可以分类设计
            field.widget.attrs={"class":"form-control","placeholder":field.label}


def users_add(request):
    if request.method == "GET":
       form=UserModelForm()  #实例化
       return render(request, "users_add.html", {"form":form})

    form=UserModelForm(data=request.POST)
    if form.is_valid():  #自动校验
        form.save()  #自动全部保存
        return redirect("/users/list/")

#   校验失败 并且在页面显示错误信息
    return render(request, "users_add.html", {"form":form})


def users_edit(request,nid):
    line_data=models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # ★加instance则自动填充line_data内容
        form=UserModelForm(instance=line_data)
        return render(request,"users_add.html", {"form":form})

    # ★加instance保存时才是修改原数据  否则是新增列
    form=UserModelForm(data=request.POST,instance=line_data)
    if form.is_valid():
        form.save()
        return redirect("/users/list/")

    return render(request,"users_add.html", {"form":form})


def users_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/users/list/")


class PrettyModelForm(forms.ModelForm):
    mobile = forms.CharField(label="号码"
      ,validators=[RegexValidator(r'^1[3-9]\d{9}$','号码长度应为11')]
    )  #限制手机号11位
    class Meta:
        model = models.PrettyNum
        fields =["mobile","price","level","status"]
       # fields="__all__"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs={"class":"form-control","placeholder":field.label}
    #验证方法二 定义clean_字段名
    def clean_mobile(self):
        # 设定mobile不能重复
        text_mobile=self.cleaned_data["mobile"]  #获取输入数据
        is_exit=models.PrettyNum.objects.filter(mobile=text_mobile).exists()
        if is_exit:
            # from django.core.exceptions import ValidationError 别的库也有valxxErr别引错
            raise ValidationError("号码重复")  #验证错误显示信息
        return text_mobile  #验证正确则返回原数据

class PrettyEditModelForm(forms.ModelForm):
    mobile=forms.CharField(disabled=True,label="号码") #设置mobile不能更改
    class Meta:
        model = models.PrettyNum
        fields =["mobile","price","level","status"]
       # fields="__all__"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs={"class":"form-control","placeholder":field.label}

def mobile_list(request):
    data_dic={}
    search_mobile=request.GET.get("search","")#后面默认值为空
    if search_mobile:
        data_dic["mobile__contains"]=search_mobile  #search有内容 搜索字典添加
                                            #此处为搜索的字典
    queryset=models.PrettyNum.objects.filter(**data_dic)
    return render(request,"mobile_list.html", {"queryset":queryset})

def mobile_add(request):
    if request.method == "GET":
        form=PrettyModelForm()
        return render(request,"mobile_add.html", {"form":form})
    form=PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/mobile/list/")
    return render(request,"mobile_add.html", {"form":form})


def mobile_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/mobile/list/")

def mobile_edit(request,nid):
    obj = models.PrettyNum.objects.get(id=nid)

    if request.method == "GET":
        form=PrettyEditModelForm(instance=obj)
        return render(request,"users_add.html", {"form":form})

    form=PrettyEditModelForm(data=request.POST,instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/mobile/list/")

    return render(request,"users_add.html", {"form":form})
