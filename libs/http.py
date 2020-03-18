import json

from django.http import HttpResponse
from django.conf import settings

from common.err import OK


def render_json(data=None, code=OK):
    result = {
        'data': data,
        'code': code
    }

    if settings.DEBUG:
        # 调试时，data 格式展开
        json_str = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        # 线上正式环境, data 为紧凑型格式
        json_str = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
    return HttpResponse(json_str, content_type='application/json')
