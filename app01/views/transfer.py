# python learning
# coding time: 2023/8/22 14:53
from django.shortcuts import render


# 跳转函数
def success(request):
    return render(request, 'success.html')


def fail(request):
    return render(request, 'fail.html')
