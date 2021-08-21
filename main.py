from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_space(num):
    return chr(32) * num


class GenerateRequest(BaseModel):
    """
    生成model及api请求对象
    """
    module_name: str
    model_file_name: str
    api_file_name: str
    fields: List[Dict]


@app.post("/generate")
async def generate(request: GenerateRequest):
    generate_models('foundation_pit_manage', '114.115.212.214', 'postgres', '96241158a0', 54323, request.model_file_name,
                    request.module_name, request.fields)
    generate_api(request.api_file_name, [request.module_name], request.module_name, request.fields)
    return "success"


@app.post("/user/login")
async def login():
    return {
        'code': 20000,
        'data': 'admin-token'
    }


@app.post("/user/info")
async def login():
    return {
        'code': 20000,
        'data': 'admin-token'
    }


def generate_models(db_name: str, host: str, user: str, password: str, port: int, module_file_name: str, module: str,
                    fields: list):
    with open('./%s.py' % module_file_name, 'a') as f:
        # import modules
        f.write('from peewee import *\n')
        f.write('from uuid import uuid4\n')
        f.write('from playhouse.pool import PooledPostgresqlDatabase\n')
        f.write('from playhouse.shortcuts import ReconnectMixin\n')
        f.write('import datetime\n\n\n')
        # config ConnObj
        f.write('class RetryPgDevDB(ReconnectMixin, PooledPostgresqlDatabase):\n')
        f.write('%s_instance = None\n\n' % get_space(4))
        f.write('%s@staticmethod\n' % get_space(4))
        f.write('%sdef get_db_instance():\n' % get_space(4))
        f.write('%sif not RetryPgDevDB._instance:\n' % get_space(8))
        f.write('%sRetryPgDevDB._instance = RetryPgDevDB(\n' % get_space(12))
        f.write('%s"%s",\n' % (get_space(16), db_name))
        f.write('%smax_connections=8,\n' % get_space(16))
        f.write('%sstale_timeout=300,\n' % get_space(16))
        f.write('%shost="%s",\n' % (get_space(16), host))
        f.write('%suser="%s",\n' % (get_space(16), user))
        f.write('%spassword="%s",\n' % (get_space(16), password))
        f.write('%sport=%d,\n' % (get_space(16), port))
        f.write('%s)\n' % get_space(12))
        f.write('%sreturn RetryPgDevDB._instance\n\n' % get_space(8))

        f.write('class %s(BaseModel):\n' % module)
        f.write('\n')
        for v in fields:
            f.write(get_space(4))
            f.write('%s = %s(' % (v['field_name'], v['field_type_class']))
            for i, j in enumerate(v['attrs']):
                f.write('%s=%s' % (j['key'], j['value']))
                if i != len(v['attrs']) - 1:
                    f.write(', ')
            f.write(')\n')
        f.write('\n')
        f.write(get_space(4))
        f.write('class Meta:\n')
        f.write(get_space(8))
        f.write("table_name = 'T_%s'" % module.upper())


def generate_api(api_file_name: str, model_names: List[str], api_name: str, fields: list):
    # 拼接需要导入的models class名称字符串
    model_names_str = ''
    for i, v in enumerate(model_names):
        model_names_str += v
        if i != len(model_names) - 1:
            model_names_str += ', '
    # 基本请求Requests
    base_request = '%sBaseRequest' % api_name
    # 查询请求QueryRequests
    query_request = '%sQueryRequest' % api_name
    # 导入模块的内容 需要request_body.py
    import_modules = 'from fastapi.encoders import jsonable_encoder\n' \
                     'from fastapi import APIRouter, Depends, Request\n' \
                     'from datetime import datetime\n' \
                     'from typing import Optional, List, Union, Any\n' \
                     'from uuid import uuid4\n' \
                     'from peewee import JOIN\n' \
                     'from models import %s\n' \
                     'from uuid import uuid1\n' \
                     'from security import check_jwt_token\n' \
                     'from request_body import get_query_params, ' \
                     'get_sort_params, %s, %s\n' \
                     'import traceback\n\n' % (model_names_str, base_request, query_request)
    if os.path.exists('%s.py' % api_file_name):
        os.remove('%s.py' % api_file_name)
    with open('%s.py' % api_file_name, 'a') as f:
        # 写入导入的包
        f.write(import_modules)
        # 写入路由对象
        f.write('router = APIRouter()\n\n')
        # 写入获取查询参数
        f.write("query_params = get_query_params(model_name='%s', props=%s.__fields__.keys())\n\n" %
                (api_name, query_request))
        # 写入获取排序参数
        f.write("sort_params = get_sort_params(model_name='%s', props=%s.__fields__.keys())\n\n\n" %
                (api_name, query_request))
        f.close()
    generate_add_def(api_name, query_request, api_file_name, fields)
    generate_delete_def(api_name, base_request, api_file_name)
    generate_update_def(api_name, query_request, api_file_name, fields)
    generate_query_def(api_name, query_request, api_file_name)


# 生成增加方法
def generate_add_def(api_name, query_request, file_name, fields):
    with open('%s.py' % file_name, 'a') as f:
        # 写入add方法
        f.write('@router.post("/add%s")\n' % api_name)
        f.write('async def add_%s(request: Request, '
                'request_param: %s, '
                'token_data: Any = Depends(check_jwt_token)):\n' % (api_name.lower(), query_request))
        # add注释
        f.write('%s"""\n' % get_space(4))
        f.write('%s添加%s\n' % (get_space(4), api_name))
        f.write('%s"""\n' % get_space(4))

        # try
        f.write('%stry:\n' % get_space(4))

        # token信息验证及commit防止异常事务卡住
        f.write('%s# 验证token\n' % get_space(8))
        f.write('%sif "user_id" not in token_data.keys():\n' % get_space(8))
        f.write('%sreturn token_data\n' % get_space(12))
        f.write('%swith db.connection_context():\n' % get_space(8))
        f.write('%s# 确保不被异常事务卡住\n' % get_space(12))
        f.write('%sdb.execute_sql("commit")\n' % get_space(12))

        # 方法体
        f.write('%s# 插入%s\n' % (get_space(12), api_name))
        f.write('%s%s = %s.insert(\n' % (get_space(12), api_name.lower(), api_name))
        # 循环字段写入
        for i, v in enumerate(fields):
            f.write('%s%s=request_param.%s' % (get_space(16), v['field_name'], v['field_name']))
            if i != len(fields) - 1:
                f.write(',\n')
            else:
                f.write('\n')
        f.write('%s)\n' % get_space(12))
        # 执行sql
        f.write('%s%s.execute()\n' % (get_space(12), api_name.lower()))

        # 返回值
        f.write('%sreturn jsonable_encoder({\n' % get_space(8))
        f.write('%s"code": 0,\n' % get_space(12))
        f.write('%s"msg": "%s add success",\n' % (get_space(12), api_name))
        f.write('%s"data": {\n' % get_space(12))
        f.write('%s"id": id\n' % get_space(16))
        f.write('%s}\n' % get_space(12))
        f.write('%s})\n' % get_space(8))

        # 异常处理
        f.write('%sexcept Exception as e:\n' % get_space(4))
        f.write('%sreturn jsonable_encoder({\n' % get_space(8))
        f.write('%s"code": 1,\n' % get_space(12))
        f.write('{}"msg": "{} add error: %s" % traceback.format_exc()\n'.format(get_space(12), api_name.lower()))
        f.write('%s})\n\n\n' % get_space(8))
        f.close()


# 生成删除方法
def generate_delete_def(api_name, base_request, file_name):
    with open('%s.py' % file_name, 'a') as f:
        # 写入add方法
        f.write('@router.post("/delete%s")\n' % api_name)
        f.write('async def delete_%s(request: Request, '
                'request_param: %s, '
                'token_data: Any = Depends(check_jwt_token)):\n' % (api_name.lower(), base_request))
        # delete注释
        f.write('%s"""\n' % get_space(4))
        f.write('%s删除%s\n' % (get_space(4), api_name))
        f.write('%s"""\n' % get_space(4))

        # try
        f.write('%stry:\n' % get_space(4))

        # token信息验证及commit防止异常事务卡住
        f.write('%s# 验证token\n' % get_space(8))
        f.write('%sif "user_id" not in token_data.keys():\n' % get_space(8))
        f.write('%sreturn token_data\n' % get_space(12))
        f.write('%swith db.connection_context():\n' % get_space(8))
        f.write('%s# 确保不被异常事务卡住\n' % get_space(12))
        f.write('%sdb.execute_sql("commit")\n' % get_space(12))

        # 方法体
        f.write('%sif request_param.ids is not None:\n' % get_space(12))
        f.write('%s# 删除%s\n' % (get_space(16), api_name))
        f.write('%s%s.delete().where(%s.id == request_param.id).execute()\n' % (get_space(16), api_name, api_name))
        f.write('%selif request_param.ids is not None:\n' % get_space(12))
        f.write('%s# 批量删除%s\n' % (get_space(16), api_name))
        f.write('%s%s.delete().where(%s.id.in_(request_param.ids)).execute()\n' % (get_space(16), api_name, api_name))

        # 返回值
        f.write('%sreturn jsonable_encoder({\n' % get_space(8))
        f.write('%s"code": 0,\n' % get_space(12))
        f.write('%s"msg": "%s delete success",\n' % (get_space(12), api_name))
        f.write('%s})\n' % get_space(8))

        # 异常处理
        f.write('%sexcept Exception as e:\n' % get_space(4))
        f.write('%sreturn jsonable_encoder({\n' % get_space(8))
        f.write('%s"code": 1,\n' % get_space(12))
        f.write('{}"msg": "{} delete error: %s" % traceback.format_exc()\n'.format(get_space(12), api_name.lower()))
        f.write('%s})\n\n\n' % get_space(8))
        f.close()


# 生成更新方法
def generate_update_def(api_name, query_request, file_name, fields):
    with open('%s.py' % file_name, 'a') as f:
        # 写入add方法
        f.write('@router.post("/update%s")\n' % api_name)
        f.write('async def update_%s(request: Request, '
                'request_param: %s, '
                'token_data: Any = Depends(check_jwt_token)):\n' % (api_name.lower(), query_request))
        # delete注释
        f.write('%s"""\n' % get_space(4))
        f.write('%s更新%s\n' % (get_space(4), api_name))
        f.write('%s"""\n' % get_space(4))

        # try
        f.write('%stry:\n' % get_space(4))

        # token信息验证
        f.write('%s# 验证token\n' % get_space(8))
        f.write('%sif "user_id" not in token_data.keys():\n' % get_space(8))
        f.write('%sreturn token_data\n' % get_space(12))

        # 方法体
        f.write('%s# 更新%s\n' % (get_space(12), api_name))
        # 检测参数中是否存在id
        f.write('%sif request_param.id is None:\n' % get_space(8))
        f.write('%sreturn jsonable_encoder({\n' % get_space(12))
        f.write('%s"code": 1,\n' % get_space(16))
        f.write('%s"msg": "update error: request_param.id is missing"\n' % get_space(16))
        f.write('%s})\n' % get_space(12))

        # 创建更新dict以及更新时间
        f.write('%sdict = {\n' % get_space(8))
        f.write('%s"update_datetime": datetime.now()\n' % get_space(12))
        f.write('%s}\n' % get_space(8))
        # 循环字段获取要更新的字段
        for i, v in enumerate(fields):
            f.write('%sif request_param.%s is not None:\n' % (get_space(8), v['field_name']))
            f.write('%sdict["%s"] = request_param.%s\n' % (get_space(12), v['field_name'], v['field_name']))
        # 执行更新操作
        f.write('%swith db.connection_context():\n' % get_space(8))
        f.write('%s# 确保不被异常事务卡住\n' % get_space(12))
        f.write('%sdb.execute_sql("commit")\n' % get_space(12))
        f.write('%s%s = %s.update(dict).where(%s.id == request_param.id)\n' %
                (get_space(12), api_name.lower(), api_name, api_name))
        f.write('%s%s.execute()\n' % (get_space(12), api_name.lower()))

        # 返回值
        f.write('%sreturn jsonable_encoder({\n' % get_space(8))
        f.write('%s"code": 0,\n' % get_space(12))
        f.write('%s"msg": "%s update success",\n' % (get_space(12), api_name))
        f.write('%s})\n' % get_space(8))

        # 异常处理
        f.write('%sexcept Exception as e:\n' % get_space(4))
        f.write('%sreturn jsonable_encoder({\n' % get_space(8))
        f.write('%s"code": 1,\n' % get_space(12))
        f.write('{}"msg": "{} update error: %s" % traceback.format_exc()\n'.format(get_space(12), api_name.lower()))
        f.write('%s})\n\n\n' % get_space(8))
        f.close()


# 生成查询方法
def generate_query_def(api_name, query_request, file_name):
    with open('%s.py' % file_name, 'a') as f:
        # 写入add方法
        f.write('@router.post("/query%s")\n' % api_name)
        f.write('async def query_%s(request: Request, '
                'request_param: %s, '
                'token_data: Any = Depends(check_jwt_token)):\n' % (api_name.lower(), query_request))
        # delete注释
        f.write('%s"""\n' % get_space(4))
        f.write('%s查询%s\n' % (get_space(4), api_name))
        f.write('%s"""\n' % get_space(4))

        # try
        f.write('%stry:\n' % get_space(4))

        # token信息验证及commit防止异常事务卡住
        f.write('%s# 验证token\n' % get_space(8))
        f.write('%sif "user_id" not in token_data.keys():\n' % get_space(8))
        f.write('%sreturn token_data\n' % get_space(12))

        # 方法体
        f.write('%s# 查询%s\n' % (get_space(8), api_name))
        # 查询peewee
        f.write('%sdata = %s.select()\n' % (get_space(8), api_name))
        # 条件查询
        f.write('%sfor key in query_params:\n' % get_space(8))
        f.write('{}if eval("request_param.%s is None" % key):\n'.format(get_space(12)))
        f.write('%scontinue\n' % get_space(16))
        f.write('{}data = eval("data.where(%s)" % query_params[key])\n'.format(get_space(12)))
        # 排序
        f.write('%sfor key in sort_params:\n' % get_space(8))
        f.write('{}if eval("request_param.%s is None" % key):\n'.format(get_space(12)))
        f.write('%scontinue\n' % get_space(16))
        f.write('{}data = eval("data.order_by(%s)" % sort_params[key])\n'.format(get_space(12)))
        # 查询返回的数量
        f.write('%scount = data.count()\n' % get_space(8))
        # 分页 如果page=-1则返回所有
        f.write('%sif request_param.page != -1:\n' % get_space(8))
        f.write('%sdata = data.paginate(request_param.page, request_param.limit)\n' % get_space(12))
        f.write('%sdata = data.dicts()\n' % get_space(8))

        # 日期格式转换
        f.write('%sfor v in data:\n' % get_space(8))
        f.write('{}v["add_datetime"] = v["add_datetime"].strftime("%Y-%m-%d")\n'.format(get_space(12)))
        f.write('{}v["update_datetime"] = v["add_datetime"].strftime("%Y-%m-%d")\n'.format(get_space(12)))

        # 返回值
        f.write('%sreturn jsonable_encoder({\n' % get_space(8))
        f.write('%s"code": 0,\n' % get_space(12))
        f.write('%s"msg": "%s query success",\n' % (get_space(12), api_name))
        f.write('%s"data": [v for v in data],\n' % get_space(12))
        f.write('%s"count": count,\n' % get_space(12))
        f.write('%s})\n' % get_space(8))

        # 异常处理
        f.write('%sexcept Exception as e:\n' % get_space(4))
        f.write('%sreturn jsonable_encoder({\n' % get_space(8))
        f.write('%s"code": 1,\n' % get_space(12))
        f.write('{}"msg": "{} update error: %s" % traceback.format_exc()\n'.format(get_space(12), api_name.lower()))
        f.write('%s})\n\n\n' % get_space(8))
        f.close()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=10002)
