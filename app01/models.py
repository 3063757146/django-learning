from django.db import models
from django.utils import timezone

class Department(models.Model):
    title = models.CharField(max_length=100)
    # 加这个函数为后面的form用  否则form输出的是类信息  这样输出title信息
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=24)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户",max_digits=10, decimal_places=2, default=0)
    # 修改此处，正确设置DateTimeField的默认值调用方式
    create_time = models.DateTimeField(verbose_name="入职时间",default=timezone.now)
    department = models.ForeignKey(verbose_name="部门",to="Department", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    gender_choise = ((1, "男"), (0, "女"))
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choise,default=1)

class PrettyNum(models.Model):
    mobile=models.CharField(verbose_name="号码",max_length=11)
    price=models.DecimalField(verbose_name="价格",max_digits=10, decimal_places=2, default=0)
    level_choices=((0,"高级"),(1,"中级"),(2,"低级"))
    level=models.SmallIntegerField(verbose_name="级别",choices=level_choices,default=1)

    status_choice=((0,"未占用"),(1,"已占用"))
    status=models.SmallIntegerField(verbose_name="状态",choices=status_choice,default=1)

