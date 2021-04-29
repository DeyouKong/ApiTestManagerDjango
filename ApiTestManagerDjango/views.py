from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import json
from APiTestManage import models
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    """ 添加、编辑用户 """
    data = request.POST
    account = data.get('account')
    password = data.get('password')
    name = data.get('name')
    status_password = data.get('statusPassword')
    role_id = data.get('role_id')
    user_id = data.get('id')
    if user_id:
        old_data = models.Users.objects.filter(id=user_id).first()
        if models.Users.objects.filter(name=name).first() and name != old_data.name:
            return JsonResponse({'msg': '名字已存在', 'status': 0})
        elif models.Users.objects.filter(account=account).first() and account != old_data.account:
            return JsonResponse({'msg': '账号已存在', 'status': 0})

        if status_password:
            if not password:
                return JsonResponse({'msg': '密码不能为空', 'status': 0})
            else:
                old_data.password = password
        old_data.name = name
        old_data.account = account
        old_data.role_id = role_id
        old_data.save()
        return JsonResponse({'msg': '修改成功', 'status': 1})
    else:
        if models.Users.objects.filter(name=name).first():
            return JsonResponse({'msg': '名字已存在', 'status': 0})
        elif models.Users.objects.filter(account=account).first():
            return JsonResponse({'msg': '账号已存在', 'status': 0})
        else:
            user = models.Users(name=name, account=account, password=password, status=1, role_id=role_id)
            user.save()
            return JsonResponse({'msg': '注册成功', 'status': 1})


class UserView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        account = data.get('account')
        password = data.get('password')
        print(account, password)
        u = models.Users.objects.get(account=account)
        token = u.token
        print(token)
        ret = {'msg': '登录成功', 'status': 1, 'token': token, 'name': account, 'userId': 1, 'roles': "1"}
        if account == '123' and password == '123':
            return Response(ret)
        else:
            return Response({'msg': '账号错误或不存在', 'status': 0})


class LogoutView(APIView):
    """退出登录"""
    def get(self, request):
        """实现退出登录逻辑"""
        logout(request)
        return Response({'msg': '登出成功', 'status': 0})


@csrf_exempt
def change_password(request):
    """ 修改密码 """
    data = request.POST
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')
    sure_password = data.get('surePassword')
    user_id = data.get('id')
    print(data)
    current_user = models.Users.objects.filter(id=user_id)
    print(current_user)
    if current_user.password != old_password:
        return JsonResponse({'msg': '旧密码错误', 'status': 0})
    if not new_password:
        return JsonResponse({'msg': '新密码不能为空', 'status': 0})
    if new_password != sure_password:
        return JsonResponse({'msg': '新密码和确认密码不一致', 'status': 0})
    # old_data = User.query.filter_by(id=user_id).first()
    current_user.password = new_password
    current_user.save()
    return JsonResponse({'msg': '密码修改成功', 'status': 1})
