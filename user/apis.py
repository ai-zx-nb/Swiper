import logging

from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from common import keys
from common import err
from libs.cache import rds
from libs.http import render_json
from user import logics
from user.models import User
from user.models import Profile
from user import forms

inflog = logging.getLogger('inf')


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.GET.get('phonenum')
    is_successed = logics.send_vcode(phonenum)

    if is_successed:
        return render_json()
    else:
        raise err.VcodeSendErr


@require_http_methods(['POST'])
def submit_vcode(request):
    '''通过验证码登录、注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 从缓存中取出验证码
    key = keys.VCODE_K % phonenum
    cached_vcode = cache.get(key)

    # 检查用户的验证码和缓存的验证码是否一直
    if vcode and vcode == cached_vcode:
        # 先获取用户
        try:
            # 如果用户存在，直接从数据库获取
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            # 如果不存在，则创建出来
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 记录用户登陆信息
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        raise err.VcodeErr


def show_profile(request):
    '''查看个人资料、交友资料'''
    key = keys.USER_RPROFILE_K % request.uid

    # 先从缓存获取数据
    result = rds.get(key, {})
    inflog.debug('从缓存获取: %s' % result)

    # 判断 result 是否是空值，如果为空，则从数据库获取数据
    if not result:
        user = User.objects.get(id=request.uid)  # 从数据库获取 user
        result.update(user.to_dict())
        result.update(user.profile.to_dict())    # 从数据库获取 profile
        inflog.debug('从数据库获取: %s' % result)
        rds.set(key, result)                     # 将结果保存到 缓存
        inflog.debug('将数据写入缓存')

    return render_json(result)


def modify_profile(request):
    '''修改个人资料、及交友资料'''
    # 定义两个 Form 表单
    user_form = forms.UserForm(request.POST)
    profile_form = forms.ProfileForm(request.POST)

    # 检查 user_form 和 profile_form
    if not user_form.is_valid() or not profile_form.is_valid():
        errors = {}
        errors.update(user_form.errors)
        errors.update(profile_form.errors)
        raise err.ProfileErr(errors)

    # 更新 user
    # update user set nickname='xxx', gender='male' where id=1;
    User.objects.filter(id=request.uid).update(**user_form.cleaned_data)

    # 更新或创建 profile
    Profile.objects.update_or_create(id=request.uid, defaults=profile_form.cleaned_data)

    # 更新缓存
    key = keys.USER_RPROFILE_K % request.uid
    rds.delete(key)

    return render_json()


def upload_avatar(request):
    '''个人照片上传'''
    avatar = request.FILES.get('avatar')  # 获取上传的文件对象
    logics.handle_avatar.delay(request.uid, avatar)
    return render_json()
