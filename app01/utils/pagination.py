# python learning
# coding time: 2023/8/21 12:43

"""
自定义分页组件(封装)
使用说明：
  一、在视图函数中：
    1.选择自己数据库中所需要分页的表单
    model_objects = models.UserInfo.objects

    2.确定搜索的内容
    search_contains = "xxx__contains"

    3.实例化分页对象
    from app01.utils.pagination import Pagination
    page_object = Pagination(request, model_objects, search__contains)
    context = {'data_list': page_object.data_list,
               'search_data': page_object.search_data,
               'page_string': page_object.page_string,
               }
    return render(request, 'xxx.html', context)

    4.可通过改变传入参数来修改页面显示的数据条数
    page_object = Pagination(request, models.Department.objects, search_contains,page_size=2)

  二、在html中
    1.搜索框（插入到与新建xx同一个位操作版面）
    <div style="float: right;width: 300px">
          <form method="get">
            <div class="input-group">
                  <input type="text" class="form-control" placeholder="Search for..." name="q" value="{{ search_data }}">
                    <span class="input-group-btn">
                        <button class="btn btn-default" type="submit">
                             <span class="glyphicon glyphicon-search" aria-hidden="true"></span>
                        </button>
                    </span>
             </div>
           </form>
        </div>


    2.循环显示的每条数据
    {% for obj in data_list %}
        {{ obj.xx }}
    {% endfor %}


    3.分页组件的实现
     <nav aria-label="Page navigation">
        <ul class="pagination">
            {{ page_string }}
        </ul>
     </nav>


"""

class Pagination(object):
    def __init__(self, request, model_objects, search_contains, page_size=10, page_param="page",
                 page_jump="jump", page_search="q"):
        # 搜索框
        data_dict = {}
        search_data = request.GET.get(page_search, '')
        if search_data:
            data_dict[search_contains] = search_data
        self.search_data = search_data

        page = request.GET.get(page_param, "1")
        if page.isdecimal():  # 判断是否是有效的十进制数
            page = int(page)
        else:
            page = 1  # 默认为第一页

        # self.page = self.page  # 当前页面
        # self.page_size = page_size  # 每页显示的数据条数

        # 起始的数据条数
        start = (page - 1) * page_size
        end = page * page_size

        # 数据总条数
        from app01 import models
        total_count = model_objects.filter(**data_dict).count()
        total_page_count, div = divmod(total_count, page_size)
        if div:  # div表示余数，如果为真则使总页数加一
            total_page_count += 1

        # 分页
        page_ = int(request.GET.get(page_param, 1))
        if request.GET.get(page_jump) == None:
            page = page_
            remain_value = ''
        else:
            try:
                jump_value = int(request.GET.get(page_jump))
                if 1 <= jump_value <= total_page_count:
                    page = int(request.GET.get(page_jump, page_))
                    remain_value = page
                else:
                    page = page_
                    remain_value = ''
            except:
                page = page_
                remain_value = ''

        # 计算出前后五页
        plus = 5
        if total_page_count <= 2 * plus + 1:
            # 数据库数据比较少
            start_page = 1
            end_page = total_page_count
        else:
            # 数据库数据比较多

            # 当前页 < 5
            if page <= plus:
                start_page = 1
                end_page = 2 * plus
            # 当前页 > 5
            elif (page + plus) > total_page_count:
                start_page = total_page_count - 2 * plus
                end_page = total_page_count
            else:
                start_page = page - plus
                end_page = page + plus

        # 初始化要插入html的数据为空
        page_str_list = []

        # 首页
        page_str_list.append('<li><a href="?page=1">首页</a></li>')

        # 上一页
        if page > 1:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
        else:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            if i == page:
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        # 下一页
        if page < total_page_count:
            next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
        else:
            next = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
        page_str_list.append(next)

        # 尾页
        page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))

        # 跳转界面
        search_string = """
                         <div style="float: right;width: 200px">
                             <form method="get">
                                 <div class="input-group">
                                     <input type="text" class="form-control" placeholder="页码" name="jump" value="{}" >
                                     <span class="input-group-btn">
                                         <button class="btn btn-default" type="submit">跳转</button>
                                     </span>
                                 </div>
                             </form>
                         </div>
                         """.format(remain_value)
        page_str_list.append(search_string)

        # 添加到html中
        from django.utils.safestring import mark_safe
        self.page_string = mark_safe("".join(page_str_list))
        self.data_list = model_objects.filter(**data_dict)[start:end]


# 以下是源码
'''
    # 搜索框
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["password__contains"] = search_data
    
    
    # 数据总条数
    total_count = models.UserInfo.objects.filter(**data_dict).count()
    total_page_count, div = divmod(total_count, 10)
    if div:  # div表示余数，如果为真则使总页数加一
        total_page_count += 1

    # 分页
    page_ = int(request.GET.get('page', 1))
    if request.GET.get('jump') == None:
        page = page_
        remain_value = ''
    else:
        jump_value = int(request.GET.get('jump'))
        if 1 <= jump_value <= total_page_count:
            page = int(request.GET.get('jump', page_))
            remain_value = page
        else:
            page = page_
            remain_value = ''

    page_size = 10          # 每页显示10条数据
    start = (page - 1) * page_size
    end = page * page_size

    # 计算出前后五页
    plus = 5
    if total_page_count <= 2 * plus + 1:
        # 数据库数据比较少
        start_page = 1
        end_page = total_page_count
    else:
        # 数据库数据比较多

        # 当前页 < 5
        if page <= plus:
            start_page = 1
            end_page = 2 * plus
        # 当前页 > 5
        elif (page + plus) > total_page_count:
            start_page = total_page_count - 2 * plus
            end_page = total_page_count
        else:
            start_page = page - plus
            end_page = page + plus

    # 初始化要插入html的数据为空
    page_str_list = []

    # 首页
    page_str_list.append('<li><a href="?page=1">首页</a></li>')

    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)

    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)

    # 下一页
    if page < total_page_count:
        next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        next = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    page_str_list.append(next)

    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))

    # 跳转界面
    search_string = """
                  <div style="float: right;width: 200px">
                      <form method="get">
                          <div class="input-group">
                              <input type="text" class="form-control" placeholder="页码" name="jump" value="{}" >
                              <span class="input-group-btn">
                                  <button class="btn btn-default" type="submit">跳转</button>
                              </span>
                          </div>
                      </form>
                  </div>
                  """.format(remain_value)
    page_str_list.append(search_string)


    # 添加到html中
    page_string = mark_safe("".join(page_str_list))
    data_list = models.UserInfo.objects.filter(**data_dict)[page_object.start:page_object.end]'''

