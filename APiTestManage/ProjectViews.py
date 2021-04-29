from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import json
from APiTestManage.models import Project
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


class ProjectView(APIView):
    def post(self, request, *args, **kwargs):
        """ 项目增加、编辑 """
        data = request.json
        project_name = data.get('projectName')
        if not project_name:
            return Response({'msg': '项目名称不能为空', 'status': 0})
        user_id = data.get('userId')
        if not user_id:
            return Response({'msg': '请选择负责人', 'status': 0})
        # principal = data.get('principal')
        environment_choice = data.get('environmentChoice')
        host = json.dumps(data.get('host'))
        host_two = json.dumps(data.get('hostTwo'))
        host_three = json.dumps(data.get('hostThree'))
        host_four = json.dumps(data.get('hostFour'))
        ids = data.get('id')
        header = data.get('header')
        variable = data.get('variable')
        func_file = json.dumps(data.get('funcFile')) if data.get('funcFile') else json.dumps([])
        # func_file='123'
        # print(func_file)
        if ids:
            old_project_data = Project.get_first(id=ids)
            if Project.get_first(name=project_name) and project_name != old_project_data.name:
                return Response({'msg': '项目名字重复', 'status': 0})
            else:
                old_project_data.name = project_name
                old_project_data.user_id = user_id
                old_project_data.environment_choice = environment_choice
                old_project_data.host = host
                old_project_data.host_two = host_two
                old_project_data.host_three = host_three
                old_project_data.host_four = host_four
                old_project_data.headers = header
                old_project_data.variables = variable
                old_project_data.func_file = func_file
                db.session.commit()
                return Response({'msg': '修改成功', 'status': 1})
        else:
            if Project.get_first(name=project_name):
                return Response({'msg': '项目名字重复', 'status': 0})
            else:
                new_project = Project(name=project_name,
                                      host=host,
                                      host_two=host_two,
                                      user_id=user_id,
                                      func_file=func_file,
                                      environment_choice=environment_choice,
                                      host_three=host_three, host_four=host_four, headers=header, variables=variable)
                db.session.add(new_project)
                db.session.commit()
                return Response({'msg': '新建成功', 'status': 1})

