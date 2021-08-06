from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request
from datetime import datetime
from typing import Optional, List, Union, Any
from uuid import uuid4
from peewee import JOIN
from models import User, Role, db
from uuid import uuid1
from security import check_jwt_token
from request_body import get_query_params, get_sort_params, UserBaseRequest, UserQueryRequest
import traceback

router = APIRouter()

query_params = get_query_params(model_name='User', props=UserQueryRequest.__fields__.keys())

sort_params = get_sort_params(model_name='User', props=UserQueryRequest.__fields__.keys())


@router.post("/addUser")
async def add_user(request: Request, request_param: UserQueryRequest, token_data: Any = Depends(check_jwt_token)):
    """
    添加User
    """
    try:
        # 验证token
        if "id" not in token_data.keys():
            return token_data
        id = uuid1().hex
        with db.connection_context():
            # 确保不被异常事务卡住
            db.execute_sql("commit")
            # 插入User
            user = User.insert(
                id=request_param.id,
                name=request_param.name,
                add_datetime=request_param.add_datetime
            )
            User.execute()
        return jsonable_encoder({
            "code": 0,
            "msg": "User add success",
            "data": {
                "id": id
            }
        })
    except Exception as e:
        return jsonable_encoder({
            "code": 1,
            "msg": "user add error: %s" % traceback.format_exc()
        })


@router.post("/deleteUser")
async def delete_user(request: Request, request_param: UserBaseRequest, token_data: Any = Depends(check_jwt_token)):
    """
    删除User
    """
    try:
        # 验证token
        if "id" not in token_data.keys():
            return token_data
        id = uuid1().hex
        with db.connection_context():
            # 确保不被异常事务卡住
            db.execute_sql("commit")
            # 删除User
            User.delete().where(User.id == request_param.id).execute()
        return jsonable_encoder({
            "code": 0,
            "msg": "User delete success",
        })
    except Exception as e:
        return jsonable_encoder({
            "code": 1,
            "msg": "user delete error: %s" % traceback.format_exc()
        })


@router.post("/updateUser")
async def update_user(request: Request, request_param: UserQueryRequest, token_data: Any = Depends(check_jwt_token)):
    """
    更新User
    """
    try:
        # 验证token
        if "id" not in token_data.keys():
            return token_data
            # 更新User
        if request_param.id is None:
            return jsonable_encoder({
                "code": 1,
                "msg": "update error: request_param.id is missing"
            })
        dict = {
            "update_datetime": datetime.now()
        }
        if request_param.id is not None:
            dict["id"] = request_param.id
        if request_param.name is not None:
            dict["name"] = request_param.name
        if request_param.add_datetime is not None:
            dict["add_datetime"] = request_param.add_datetime
        with db.connection_context():
            # 确保不被异常事务卡住
            db.execute_sql("commit")
            user = User.update(dict).where(User.id == request_param.id)
            user.execute()
        return jsonable_encoder({
            "code": 0,
            "msg": "User update success",
        })
    except Exception as e:
        return jsonable_encoder({
            "code": 1,
            "msg": "user update error: %s" % traceback.format_exc()
        })


@router.post("/queryUser")
async def query_user(request: Request, request_param: UserQueryRequest, token_data: Any = Depends(check_jwt_token)):
    """
    查询User
    """
    try:
        # 验证token
        if "id" not in token_data.keys():
            return token_data
        # 查询User
        data = User.select()
        for key in query_params:
            if eval("request_param.%s is None" % key):
                continue
            data = eval("data.where(%s)" % query_params[key])
        for key in sort_params:
            if eval("request_param.%s is None" % key):
                continue
            data = eval("data.order_by(%s)" % sort_params[key])
        count = data.count()
        if request_param.page != -1:
            data = data.paginate(request_param.page, request_param.limit)
        data = data.dicts()
        for v in data:
            v["add_datetime"] = v["add_datetime"].strftime("%Y-%m-%d")
            v["update_datetime"] = v["add_datetime"].strftime("%Y-%m-%d")
        return jsonable_encoder({
            "code": 0,
            "msg": "User query success",
            "data": [v for v in data],
            "count": count,
        })
    except Exception as e:
        return jsonable_encoder({
            "code": 1,
            "msg": "user update error: %s" % traceback.format_exc()
        })


