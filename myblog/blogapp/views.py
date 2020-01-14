from django.views.generic import View
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator

from .models import CustomUser, Blog, BlogType, Comment
from .tools.render_mako import render_to_response
from .tools.custom_decorator import login_dec


class Index(View):
    """博客首页"""
    tempalte_name = 'BlogApp/index.html'

    def get(self, request):
        return render_to_response(request, self.tempalte_name)


class Login(View):
    """登录页面"""
    template_name = 'BlogApp/login.html'

    @login_dec()
    def get(self, request):
        return render_to_response(request, self.template_name)

    def post(self, request):
        input_date = {}
        output_data = {'error': ''}

        # 循环取出表单中需要的值
        for key, value in request.POST.items():
            if key in ['username', 'password']:
                input_date[key] = value

        # 验证用户是否存在
        if not CustomUser.objects.filter(username=input_date['username']).exists():
            output_data['error'] = '用户名不存在'
            return render_to_response(request, self.template_name, output_data)

        # 判断用户密码是否正确
        user = authenticate(request, username=input_date['username'], password=input_date['password'])
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            output_data['error'] = '密码错误！'
            return render_to_response(request, self.template_name, output_data)


class LogoutUser(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class RegisterUser(View):
    """用户注册页面"""

    template_name = 'BlogApp/register.html'

    @login_dec()
    def get(self, request):
        return render_to_response(request, self.template_name)

    def post(self, request):
        input_data = {}
        output_data = {'error': ''}
        # 获取用户输入的值
        for key, value in request.POST.items():
            if key in ['username', 'email', 'password', 'check_pass']:
                input_data[key] = value

        # 判断用户名是否存在
        if CustomUser.objects.filter(username__exact=input_data.get('username')):
            output_data['error'] = '该用户名已存在'
            return render_to_response(request, self.template_name, output_data)
        # 判断邮箱是否已经使用
        if CustomUser.objects.filter(email__exact=input_data.get('email')):
            output_data['error'] = '该邮箱已使用'
            return render_to_response(request, self.template_name, output_data)
        # 判断两次密码是否一致
        if not input_data['password'] == input_data['check_pass']:
            output_data['error'] = '两次密码不一致'
            return render_to_response(request, self.template_name, output_data)

        user = CustomUser.objects.create_user(
            username=input_data.get('username'),
            email=input_data.get('email'),
            password=input_data.get('password')
        )

        return redirect(reverse('login'))


class BlogView(View):
    """博客列表页"""
    template_name = 'BlogApp/blog.html'

    def get(self, request):
        input_data = {}
        output_data = {}
        output_data['blog_list'] = Blog.objects.all().order_by('-create_time')
        output_data['blog_top'] = Blog.get_hot_blog()

        paginator = Paginator(output_data['blog_list'], 6)

        output_data['blog_paginator'] = paginator.get_page(request.GET.get('page', ''))

        return render_to_response(request, self.template_name, output_data)


class BlogDetails(View):
    """博客详情页"""
    template_name = 'BlogApp/blog_details.html'

    def get(self, request, blog_id):
        # 如果传入的博客ID存在则返回对应的详情页面
        # 如果不存在则跳转到博客列表页面
        output_date = {'error': request.GET.get('error', '')}
        try:
            blog = Blog.objects.get(pk=blog_id)
            comments = Comment.objects.filter(blog=blog_id)
            related_blog = Blog.objects.filter(Q(pk=(blog_id - 1)) | Q(pk=(blog_id + 1)))
            output_date = {
                'blog': blog,
                'comments': comments,
                'blog_top': Blog.get_hot_blog(),
                'related_blog': related_blog
            }
            blog.page_view += 1
            blog.save()
        except Exception as e:
            print(e)
            return redirect(reverse('blog_list'))
        return render_to_response(request, self.template_name, output_date)

    def post(self, request, blog_id):
        input_data = {}
        output_data = {}
        for key, value in request.POST.items():
            if key in ['username', 'email', 'usercomment']:
                input_data[key] = value

        try:
            com = Comment.objects.create(
                username=input_data['username'],
                email=input_data['email'],
                content=input_data['usercomment'],
                blog=Blog.objects.get(pk=blog_id),
            )
        except Exception as e:
            print(e)
            output_data['error'] = '发表评论失败'
            return redirect("{0}?error={1}".format(reverse('blog_details', kwargs={'blog_id': blog_id}), '发表评论失败'))

        return redirect(reverse('blog_details', kwargs={'blog_id': blog_id}))


class PhotoView(View):
    """照片墙页面"""
    template_name = 'BlogApp/photo.html'

    def get(self, request):
        return render_to_response(request, self.template_name)


class MyCenter(View):
    """个人中心页面"""

    template_name = 'BlogApp/my_center.html'

    @login_dec(status=False)
    def get(self, request):
        user_blog = Blog.objects.filter(user_id=request.user.id).order_by('-create_time')
        paginator = Paginator(user_blog, 5)
        output_data = {'user_blog_list': paginator.get_page(request.GET.get('page', ''))}
        return render_to_response(request, self.template_name, output_data)


class BlogPublish(View):
    """博客发表页面视图"""

    template_name = 'BlogApp/blog_publish.html'

    @login_dec(status=False)
    def get(self, request):
        output_data = {
            'blog_type': BlogType.objects.all(),
        }
        return render_to_response(request, self.template_name, output_data)

    def post(self, request):

        input_data = {'user_id': request.user.id}
        for key, value in request.POST.items():
            if key in ['title', 'blog_type', 'cover', 'content']:
                input_data[key] = value

        print(input_data['cover'])
        try:
            blog = Blog.objects.create(
                user=CustomUser.objects.get(pk=input_data['user_id']),
                type=BlogType.objects.get(name=input_data['blog_type']),
                title=input_data['title'],
                cover=input_data['cover'],
                content=input_data['content']
            )
        except Exception as e:
            print(e)
            output_data = {'error': '添加博客失败', 'blog_type': BlogType.objects.all()}
            return render_to_response(request, self.template_name, output_data)

        return redirect(reverse('my_center'))


class UpdateBlog(View):
    template_name = 'BlogApp/update_blog.html'

    @login_dec(status=False)
    def get(self, request, update_blog_id):
        try:
            output_data = {'update_blog': Blog.objects.get(pk=update_blog_id), 'blog_type': BlogType.objects.all()}

        except Exception as e:
            print(e)
            return redirect(reverse('my_center'))

        return render_to_response(request, self.template_name, output_data)

    def post(self, request, update_blog_id):

        input_data = {'up_id': int(request.POST.get('up_id'))}

        if update_blog_id != input_data['up_id']:
            print('不匹配ID')
            return redirect(reverse('my_center'))

        for key, value in request.POST.items():
            if key in ['title', 'type', 'content', 'cover']:
                input_data[key] = value

        try:
            up_blog = Blog.objects.get(pk=input_data['up_id'])

            up_blog.title = input_data['title']
            up_blog.type = BlogType.objects.get(name=input_data['type'])
            up_blog.content = input_data['content']
            up_blog.cover = input_data['cover']
            up_blog.save()
            print(Blog.objects.get(pk=input_data['up_id']))

        except Exception as e:
            print(e)

        return redirect(reverse('my_center'))
