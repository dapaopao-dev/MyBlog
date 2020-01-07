from mako.lookup import TemplateLookup

# 引入Django下的：RequestContext（请求上下文），settings（项目配置文件），Context（上下文内容），HttpResponse（响应对象）
from django.template import RequestContext
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse
from django.middleware.csrf import get_token


def render_to_response(request, template, data=None):
    """这是一个重定义的模板渲染方法，使用的是mako模板引擎"""

    context_instance = RequestContext(request)

    path = settings.TEMPLATES[0]['DIRS'][0]

    # mako的模板对象
    lookup = TemplateLookup(
        directories=[path],
        output_encoding='utf-8',
        input_encoding='utf-8'
    )

    # mako的模板对象
    mako_tempalte = lookup.get_template(template)

    if not data:
        data = {}

    if context_instance:
        context_instance.update(data)
    else:
        context_instance = Context(data)

    result = {}

    for d in context_instance:
        result.update(d)

    # 跨域密钥，mako好像没有，麻烦的得自己写，虽然我也不会写，都是抄的
    result['request'] = request
    request.META['CSRF_TOKEN'] = get_token(request)
    result['csrf_token'] = (
        '<div style="display:none">'
        '<input type="hidden" '
        'name="csrfmiddlewaretoken" '
        'value="{0}" />'
        '</div>'.format(request.META['CSRF_COOKIE']))

    return HttpResponse(mako_tempalte.render(**result))
