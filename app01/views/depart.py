# python learning
# coding time: 2023/8/22 14:51
from django.shortcuts import render, redirect

from app01 import models


# 部门函数
def depart_list(request):
    ''' 部门列表 '''
    from app01.utils.pagination import Pagination
    search_contains = "title__contains"
    page_object = Pagination(request, models.Department.objects, search_contains, page_size=2)
    context = {'data_list': page_object.data_list,
               'search_data': page_object.search_data,
               'page_string': page_object.page_string,
               }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    ''' 新建部门 '''
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    depart_name = request.POST.get('title')
    models.Department.objects.create(title=depart_name)
    return redirect('/success/')


def depart_delete(request):
    ''' 删除部门 '''
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/success/')


def depart_edit(request, nid):
    data_list = models.Department.objects.all()
    edit_one = models.Department.objects.filter(id=nid)
    print(data_list)
    print(edit_one)
    if request.method == 'GET':
        return render(request, 'depart_edit.html', {'data_list': data_list, 'nid': nid, 'one': edit_one})
    edit_title = request.POST.get('title')
    print(edit_title)
    models.Department.objects.filter(id=nid).update(title=edit_title)
    return redirect('/success/')
