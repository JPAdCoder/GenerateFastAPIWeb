from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from jose.exceptions import ExpiredSignatureError, JWTError
from fastapi.encoders import jsonable_encoder
from fastapi import Header

# 使用装饰器进行登录验证
from functools import wraps

SECRET_KEY = "2]pqc{Be$C6`sw@r"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(id: str, expires_delta: timedelta = None) -> str:
    """
    生成token
    :param id: token中携带的参数
    :param expires_delta: 过期时间间隔
    :return:
    """
    global SECRET_KEY
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"exp": expire, "id": id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, "HS256")
    return encoded_jwt


def check_jwt_token(token: Optional[str] = Header(None, alias="Authentication")) -> Any:
    """
    验证token
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return payload
    except ExpiredSignatureError as e:
        return jsonable_encoder({
            "code": 2,
            "msg": "token 过时"
        })
    except JWTError as e:
        return jsonable_encoder({
            "code": 3,
            "msg": "token 错误"
        })
    except AttributeError as e:
        return jsonable_encoder({
            "code": 4,
            "msg": "缺少token信息"
        })


def check_hash(plain_password: str, hashed_password: str) -> bool:
    """
    检验密码hash一致性
    :param plain_password:
    :param hashed_password:
    :return:
    """
    global pwd_context
    return pwd_context.verify(plain_password, hashed_password)



