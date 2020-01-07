from django.db import models
from django.contrib.auth.models import AbstractUser


# 需要设计的模型：博客模型，分类模型，扩展的用户模型，评论模型。图片模型
# 模型之间的关系：用户-博客，分类-博客，博客-评论，用户-评论

class CustomUser(AbstractUser):
    """一个自定义的用户模型，在内置模型的基础上会扩展一些字段：头像"""

    def __str__(self):
        return "自定义的用户模型"


class BlogType(models.Model):
    """分类模型"""
    name = models.CharField(max_length=18, null=True, verbose_name='分类')

    def __str__(self):
        return "分类模型"


class Blog(models.Model):
    """自定义的博客模型"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog', verbose_name='作者')
    title = models.CharField(max_length=50, blank=False, unique=True, verbose_name='标题')
    content = models.TextField(blank=False, verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    page_view = models.IntegerField(default=0, verbose_name='浏览量')
    enjoy = models.IntegerField(default=0, verbose_name='点赞量')
    type = models.ForeignKey(BlogType, on_delete=models.SET_NULL, null=True, related_name='blog', verbose_name='博客分类')

    def get_hot_blog(self):
        """返回最热门的前三博客内容"""
        return Blog.objects.order_by('page_view', 'enjoy')[:3]

    def __str__(self):
        return "自定义的博客模型"


class Comment(models.Model):
    """自定义的一个评论模型"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment', verbose_name='评论用户')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment', verbose_name='评论博客')
    content = models.CharField(max_length=300, blank=False, verbose_name='评论内容')
    enjoy = models.IntegerField(default=0, verbose_name='点赞量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    def __str__(self):
        return "自定义的评论模型"
