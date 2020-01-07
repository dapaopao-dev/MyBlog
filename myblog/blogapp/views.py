from django.shortcuts import render
from django.views.generic import View
from .tools.render_mako import render_to_response
from django.shortcuts import redirect, reverse
from .models import CustomUser


class Index(View):
    """博客首页"""
    tempalte_name = 'BlogApp/index.html'

    def get(self, request):
        return render_to_response(request, self.tempalte_name)


class Login(View):
    """登录页面"""
    template_name = 'BlogApp/login.html'

    def get(self, request):
        return render_to_response(request, self.template_name)


class RegisterUser(View):
    """用户注册页面"""

    template_name = 'BlogApp/register.html'

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
        return render_to_response(request, self.template_name)


class BlogDetails(View):
    """博客详情页"""
    template_name = 'BlogApp/blog_details.html'

    def get(self, request):
        return render_to_response(request, self.template_name)


class PhotoView(View):
    """照片墙页面"""
    template_name = 'BlogApp/photo.html'

    def get(self, request):
        return render_to_response(request, self.template_name)
