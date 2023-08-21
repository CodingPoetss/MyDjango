from django.db import models

# Create your models here.
class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)
    def __str__(self):
        return self.title           # 实例化对象时输出的是地址,__str__(self)可以打印具体的地址

class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')
    ''' 有约束，默认为depart_id '''
    ''' 置空 '''
    # depart = models.ForeignKey(verbose_name='所属部门', to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)
    depart = models.ForeignKey(verbose_name='所属部门', to='Department', to_field='id', on_delete=models.PROTECT)

class PrettyNum(models.Model):
    """ 靓号管理 """
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)
    level_choices = (
        (1, 'senior'),
        (2, 'medium'),
        (3, 'primary'),
    )
    level = models.SmallIntegerField(verbose_name='等级', choices=level_choices)
    status_choices = (
        (1, 'occupied'),
        (2, 'empty'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)