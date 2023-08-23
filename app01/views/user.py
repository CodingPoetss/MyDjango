# python learning
# coding time: 2023/8/22 14:51
from django import forms
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.Bootstrap import BootStrapModelForm

# 用户函数
def user_list(request):
    # 封装类
    from app01.utils.pagination import Pagination
    search_contains = "password__contains"
    page_object = Pagination(request, models.UserInfo.objects, search_contains)
    context = {'data_list': page_object.data_list,
               'search_data': page_object.search_data,
               'page_string': page_object.page_string,
               }
    return render(request, 'user_list.html', context)

def user_add(request):
    """ 添加用户（原始方式） """
    departs = models.Department.objects.all()
    context = {
        'gender_choices': models.UserInfo.gender_choices,
        'depart_list': models.Department.objects.all(),
    }
    if request.method == 'GET':
        return render(request, 'user_add.html', context)
    name = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    gender_id = request.POST.get('gender')
    depart_id = request.POST.get('depart')   # 得到的是字符串
    depart_instance = models.Department.objects.get(pk=depart_id)  # 得到department的外键实例
    models.UserInfo.objects.create(name=name, password=password, age=age, account=account, create_time=create_time,
                                   gender=gender_id, depart=depart_instance)
    return redirect('/success/')

class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3,
                           label='用户名',
                           widget=forms.TextInput(attrs={'class': 'form-control'})
     )
    password = forms.CharField(max_length=10, label='密码')
    # widgets = {
    #     "create-time":forms.TextInput("type":"date")
    # }
    class Meta:
        model = models.UserInfo  # 选择的model模板类
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart', ]  # 选择类中的元素


def user_model_form_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/success/')
    else:
        return render(request, 'user_model_form_add.html', {'form': form})

class UserModelForm_Default(forms.ModelForm):
    name = forms.CharField(min_length=3, label='用户名')
    password = forms.CharField(max_length=10, label='密码')
    class Meta:
        model = models.UserInfo                     # 选择的model模板类
        fields = ['name', 'password', 'age', 'gender', 'account', 'create_time', 'depart', ]        # 选择类中的元素
def user_edit(request, nid):
    data_list = models.UserInfo.objects.all()
    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm_Default(instance=row_object)
    if request.method == 'GET':
        return render(request, 'user_edit.html', {'form': form, 'nid': nid, 'data_list': data_list})
    form = UserModelForm_Default(data=request.POST, instance=row_object)
    if form.is_valid():
        # form.instance.password = 0            # 可手动设置保存
        form.save()
        return redirect('/success/')
    else:
        return render(request, 'user_edit.html', {'form': form, 'nid': nid, 'data_list': data_list})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/success')