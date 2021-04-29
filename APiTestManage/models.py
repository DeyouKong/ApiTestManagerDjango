from django.db import models
from django.contrib.auth.models import AbstractUser
# import datetime
from ApiTestManagerDjango import settings
import jwt
from datetime import datetime, timedelta

# Create your models here.


class Users(models.Model):
    __doc__ = "用户表"
    db_table = 'users'
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=32, unique=True, verbose_name='账号')
    password = models.CharField(max_length=128, verbose_name='密码')
    name = models.CharField(max_length=64, verbose_name='姓名')
    status = models.IntegerField(default=1, verbose_name='状态，1为启用，2为冻结')
    role_id = models.IntegerField(default=1, verbose_name='所属的角色id')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.account

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'id': self.id,
            'account': self.account,
            'name': self.name,
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class BaseModel(models.Model):
    """ 基类模型 """
    __abstract__ = True

    id = models.AutoField(primary_key=True)
    is_delete = models.SmallIntegerField(default=0, verbose_name='通过更改状态来判断记录是否被删除, 0数据有效, 1数据已删除')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)


class Role(models.Model):
    __doc__ = "角色表"
    db_table = 'role'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=100, null=True)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name


class Permission(models.Model):
    __doc__ = "权限表"
    db_table = 'permission'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    # role = models.ForeignKey('Role', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = verbose_name


class Project(BaseModel):
    __doc__ = "项目表"
    db_table = 'project'
    user_id = models.IntegerField(verbose_name='所属的用户id')
    name = models.CharField(max_length=24, unique=True, verbose_name='项目名称')
    host = models.CharField(max_length=1024, verbose_name='测试环境')
    host_two = models.CharField(max_length=1024, verbose_name='开发环境')
    host_three = models.CharField(max_length=1024, verbose_name='线上环境')
    host_four = models.CharField(max_length=1024, verbose_name='备用环境')
    environment_choice = models.CharField(max_length=16, verbose_name='环境选择，first为测试，以此类推')
    principal = models.CharField(max_length=16)
    variables = models.CharField(max_length=2048, verbose_name='项目的公共变量')
    headers = models.CharField(max_length=1024, verbose_name='项目的公共头部信息')
    func_file = models.CharField(max_length=128, verbose_name='函数地址')
    modules = models.ForeignKey('Module', on_delete=models.CASCADE)
    configs = models.ForeignKey('Config', on_delete=models.CASCADE)
    case_sets = models.ForeignKey('CaseSet', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目表"
        verbose_name_plural = verbose_name


class Module(models.Model):
    __doc__ = "接口模块表"
    db_table = 'module'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='接口模块')
    num = models.IntegerField(null=True, verbose_name='模块序号')
    project_id = models.ForeignKey("Project", verbose_name='所属的项目id', on_delete=models.CASCADE)
    api_msg = models.ForeignKey('ApiMsg', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "接口模块表"
        verbose_name_plural = verbose_name


class Config(models.Model):
    __doc__ = "配置信息表"
    db_table = 'config'
    id = models.AutoField(primary_key=True)
    num = models.IntegerField(verbose_name='配置序号')
    name = models.CharField(max_length=128, verbose_name='配置名称')
    variables = models.TextField(verbose_name='配置参数')
    func_address = models.CharField(max_length=128, verbose_name='配置函数')
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name='所属的项目id')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "配置名称表"
        verbose_name_plural = verbose_name


class CaseSet(models.Model):
    __doc__ = "用例集"
    db_table = 'case_set'
    id = models.AutoField(primary_key=True)
    num = models.IntegerField(verbose_name='用例集合序号')
    name = models.CharField(max_length=128, verbose_name='用例集名称')
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name='所属的项目id')
    cases = models.ForeignKey('Case', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用例集"
        verbose_name_plural = verbose_name


class Case(BaseModel):
    __doc__ = "用例"
    db_table = 'case'
    num = models.IntegerField(verbose_name='用例序号')
    name = models.CharField(max_length=128, verbose_name='用例名称')
    desc = models.CharField(max_length=256, verbose_name='用例描述')
    func_address = models.CharField(max_length=256, verbose_name='用例需要引用的函数')
    variable = models.TextField(null=True, verbose_name='用例公共参数')
    times = models.IntegerField(verbose_name='执行次数')
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name='所属的项目id')
    case_set_id = models.ForeignKey("CaseSet", on_delete=models.CASCADE, verbose_name='所属的用例集id')
    environment = models.IntegerField(verbose_name='环境类型')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用例"
        verbose_name_plural = verbose_name


class ApiMsg(models.Model):
    __doc__ = "接口信息"
    db_table = 'api_msg'
    id = models.AutoField(primary_key=True)
    num = models.IntegerField(verbose_name='接口序号')
    name = models.CharField(max_length=128, verbose_name='接口名称')
    desc = models.CharField(max_length=256, verbose_name='接口描述')
    variable_type = models.CharField(max_length=32, verbose_name='参数类型选择')
    status_url = models.CharField(max_length=32, verbose_name='基础url,序号对应项目的环境')
    up_func = models.CharField(max_length=128, verbose_name='接口执行前的函数')
    down_func = models.CharField(max_length=128, verbose_name='接口执行后的函数')
    method = models.CharField(max_length=32, verbose_name='请求方式')
    variable = models.TextField(verbose_name='form-data形式的参数')
    json_variable = models.TextField(verbose_name='json形式的参数')
    param = models.TextField(verbose_name='url上面所带的参数')
    url = models.CharField(max_length=256, verbose_name='接口地址')
    skip = models.CharField(max_length=128, verbose_name='跳过判断')
    extract = models.CharField(max_length=2048, verbose_name='提取信息')
    validate = models.CharField(max_length=2048, verbose_name='断言信息')
    header = models.CharField(max_length=2048, verbose_name='头部信息')
    module_id = models.ForeignKey("Module", on_delete=models.CASCADE, verbose_name='所属的接口模块id')
    project_id = models.IntegerField(verbose_name='所属的项目id')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "接口信息"
        verbose_name_plural = verbose_name


class CaseData(models.Model):
    __doc__ = "测试步骤"
    db_table = 'case_data'
    id = models.AutoField(primary_key=True)
    num = models.IntegerField(verbose_name='步骤序号，执行顺序按序号来')
    status = models.CharField(max_length=16, verbose_name='状态，true表示执行，false表示不执行')
    name = models.CharField(max_length=128, verbose_name='步骤名称')
    up_func = models.CharField(max_length=256, verbose_name='步骤执行前的函数')
    down_func = models.CharField(max_length=256, verbose_name='步骤执行后的函数')
    skip = models.CharField(max_length=64, verbose_name='跳过判断函数')
    time = models.IntegerField(default=1, verbose_name='执行次数')
    param = models.TextField(default=u'[]')
    status_param = models.CharField(max_length=64, default=u'[true, true]')
    variable = models.TextField()
    json_variable = models.TextField()
    status_variables = models.CharField(max_length=64)
    extract = models.CharField(max_length=2048)
    status_extract = models.CharField(max_length=64)
    validate = models.CharField(max_length=2048)
    status_validate = models.CharField(max_length=64)
    header = models.CharField(max_length=2048)
    status_header = models.CharField(max_length=64)
    case_id = models.ForeignKey("Case", on_delete=models.CASCADE)
    api_msg_id = models.ForeignKey("ApiMsg", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "测试步骤"
        verbose_name_plural = verbose_name


class Report(models.Model):
    __doc__ = "测试报告"
    db_table = 'report'
    id = models.AutoField(primary_key=True)
    case_names = models.CharField(max_length=128, verbose_name='用例的名称集合')
    read_status = models.CharField(max_length=16, verbose_name='阅读状态')
    performer = models.CharField(max_length=16, verbose_name='执行者')
    project_id = models.CharField(max_length=16)
    result = models.CharField(max_length=16, verbose_name='结果')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "测试报告"
        verbose_name_plural = verbose_name


class Task(models.Model):
    __doc__ = "定时任务"
    db_table = 'tasks'
    id = models.AutoField(primary_key=True)
    num = models.IntegerField(verbose_name='任务序号')
    task_name = models.CharField(max_length=64, verbose_name='任务名称')
    task_config_time = models.CharField(max_length=256, verbose_name='cron表达式')
    set_id = models.CharField(max_length=2048)
    case_id = models.CharField(max_length=2048)
    task_type = models.CharField(max_length=16)
    task_to_email_address = models.CharField(max_length=256, verbose_name='收件人邮箱')
    task_send_email_address = models.CharField(max_length=256, verbose_name='发件人邮箱')
    email_password = models.CharField(max_length=256, verbose_name='发件人邮箱密码')
    status = models.CharField(max_length=16, default=u'创建', verbose_name='任务的运行状态，默认是创建')
    project_id = models.CharField(max_length=16)
    send_email_status = models.CharField(max_length=16)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.task_name

    class Meta:
        verbose_name = "定时任务"
        verbose_name_plural = verbose_name


class TestCaseFile(models.Model):
    __doc__ = "测试用例文件序"
    db_table = 'test_case_file'
    id = models.AutoField(primary_key=True)
    num = models.IntegerField(verbose_name='测试用例文件序号')
    name = models.CharField(max_length=32, verbose_name='测试用例文件名称')
    status = models.IntegerField(verbose_name='0代表文件夹；1代表用例文件')
    higher_id = models.IntegerField(verbose_name='上级id，父级为0')
    user_id = models.IntegerField(verbose_name='创建人id')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "测试用例文件"
        verbose_name_plural = verbose_name


class FuncFile(models.Model):
    __doc__ = "内置函数"
    db_table = 'func_file'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name='内置函数文件名称')
    num = models.IntegerField(verbose_name='内置函数文件序号')
    status = models.IntegerField(verbose_name='0代表文件夹；1代表用例文件')
    higher_id = models.IntegerField(verbose_name='上级id，父级为0')
    user_id = models.IntegerField(verbose_name='创建人id')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "内置函数"
        verbose_name_plural = verbose_name


class Logs(models.Model):
    __doc__ = "日志"
    db_table = 'logs'
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=128, verbose_name='ip')
    uid = models.CharField(max_length=128, verbose_name='uid')
    url = models.CharField(max_length=128, verbose_name='url')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "日志"
        verbose_name_plural = verbose_name
