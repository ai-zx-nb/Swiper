"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from user import apis as user_api
from social import apis as social_api


urlpatterns = [
    path('api/user/get_vcode', user_api.get_vcode),
    path('api/user/submit_vcode', user_api.submit_vcode),
    path('api/user/show_profile', user_api.show_profile),
    path('api/user/modify_profile', user_api.modify_profile),
    path('api/user/upload_avatar', user_api.upload_avatar),

    path('api/social/rcmd_user', social_api.rcmd_user),
    path('api/social/like', social_api.like),
    path('api/social/superlike', social_api.superlike),
    path('api/social/dislike', social_api.dislike),
    path('api/social/rewind', social_api.rewind),
    path('api/social/show_users_liked_me', social_api.show_users_liked_me),
    path('api/social/friends', social_api.friends),
    path('api/social/hot_rank', social_api.hot_rank),
]
