from django.db import models
from django.contrib.auth.models import AbstractUser


# 需要设计的模型：博客模型，分类模型，扩展的用户模型，评论模型。图片模型
# 模型之间的关系：用户-博客，分类-博客，博客-评论，用户-评论

class CustomUser(AbstractUser):
    """一个自定义的用户模型，在内置模型的基础上会扩展一些字段：头像"""

    def __str__(self):
        return self.username


class BlogType(models.Model):
    """分类模型"""
    name = models.CharField(max_length=18, null=True, verbose_name='分类')

    def __str__(self):
        return self.name


class Blog(models.Model):
    """自定义的博客模型"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog', verbose_name='作者')
    title = models.CharField(max_length=50, blank=False, unique=True, verbose_name='标题')
    content = models.TextField(blank=False, verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    page_view = models.IntegerField(default=0, verbose_name='浏览量')
    enjoy = models.IntegerField(default=0, verbose_name='点赞量')
    type = models.ForeignKey(BlogType, on_delete=models.SET_NULL, null=True, related_name='blog', verbose_name='博客分类')
    cover = models.CharField(max_length=200, default='...', verbose_name='封面')
    status = models.BooleanField(default=False, verbose_name='博客状态')
    illustrations = models.CharField(max_length=600, verbose_name='插图', blank=True)

    @classmethod
    def get_hot_blog(cls):
        """返回最热门的前三博客内容"""
        return cls.objects.order_by('page_view', 'enjoy')[:3]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """自定义的一个评论模型"""
    username = models.CharField(max_length=30, blank=False, default='', verbose_name='评论名')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment', verbose_name='评论博客')
    content = models.CharField(max_length=300, blank=False, verbose_name='评论内容')
    enjoy = models.IntegerField(default=0, verbose_name='点赞量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    email = models.EmailField(default='')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.content
