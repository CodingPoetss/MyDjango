# python learning
# coding time: 2023/8/23 12:07
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination


def admin_list(request):
    data_list = models.Admin.objects.all()
    model_objects = models.Admin.objects
    search_contains = "name__contains"
    page_object = Pagination(request, model_objects, search_contains)
    context = {'data_list': page_object.data_list,
               'search_data': page_object.search_data,
               'page_string': page_object.page_string,
               }
    return render(request, 'admin_list.html', context)
