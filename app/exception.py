from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = '服务器错误'
    error_code = 9999

    def __init__(self, msg=None, code=None, error_code=None):
        if msg:
            self.msg = msg
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code

        super().__init__(description=msg, response=None)

    def get_body(self, environ=None, scope=None):
        body = dict(
            msg=self.msg,
            code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        return json.dumps(body)

    def get_headers(self, environ=None, scope=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        return request.full_path.split('?')[0]


# @formatter:off
#####################################
# 200
Success             = type('Success',           (APIException,), {'code': 200, 'msg': 'Success', 'error_code': 0})

#####################################
# 400
ParameterError      = type('ParameterError',    (APIException,), {'code': 400, 'msg': '参数错误', 'error_code': 1000})
PasswordError       = type('PasswordError',     (APIException,), {'code': 400, 'msg': '密码错误', 'error_code': 1001})
StatusError         = type('StatusError',       (APIException,), {'code': 400, 'msg': '状态错误', 'error_code': 1002})
CantGetNumber       = type('CantGetNumber',     (APIException,), {'code': 400, 'msg': '取号失败', 'error_code': 1003})
NotLogin            = type('NotLogin',          (APIException,), {'code': 401, 'msg': '未登录', 'error_code': 2000})
NoPermissionError   = type('NoPermissionError', (APIException,), {'code': 401, 'msg': '资源无权限', 'error_code': 2001})
NotFoundError       = type('NotFoundError',     (APIException,), {'code': 404, 'msg': '资源未找到', 'error_code': 3000})
ConflictError       = type('ConflictError',     (APIException,), {'code': 409, 'msg': '资源已存在', 'error_code': 4000})

#####################################
# 500
ServerError         = type('ServerError',       (APIException,), {})
ThirdAPIError       = type('ThirdAPIError',     (APIException,), {'code': 500, 'msg': '第三方API错误', 'error_code': 9001})
DBError             = type('DBError',           (APIException,), {'code': 500, 'msg': '数据库错误', 'error_code': 9002})

#####################################
# Program Exception
ConfigException = type('ConfigException', (Exception,), {'message': '配置文件出错'})
