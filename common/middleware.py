'''
中间件: 面向切面编程

    流水线: A -> B --> C -> D -> E ...
                   ^
                   |
                  检查
'''
import logging

from django.utils.deprecation import MiddlewareMixin

from libs.http import render_json
from common import err

errlog = logging.getLogger('err')


class AuthMiddleware(MiddlewareMixin):
    '''检查用户登陆状态中间件'''
    white_list = [
        '/api/user/get_vcode',
        '/api/user/submit_vcode',
        '/api/social/hot_rank',
    ]

    def process_request(self, request):
        # 检查当前的请求是否在白名单中
        if request.path in self.white_list:
            return

        # 检查用户是否登陆
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=err.LoginRequired.code)
        else:
            request.uid = uid


class StatusCodeMiddleware(MiddlewareMixin):
    '''状态码处理中间件'''
    def process_exception(self, request, exception):
        if isinstance(exception, err.LogicError):
            errlog.warning(f'LogicError: {exception.code} : {exception.data}')
            return render_json(exception.data, exception.code)
