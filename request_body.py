from pydantic import BaseModel, Field
from typing import Optional, List


class BaseRequest(BaseModel):
    """
    基础请求对象
    """
    id: Optional[str] = Field(
        None,
        description="表id"
    )
    ids: Optional[List[str]] = Field(
        None,
        description="表id集合，批量删除时使用"
    )
    remarks: Optional[str] = Field(
        None,
        description="备注"
    )
    add_datetime: Optional[str] = Field(
        None,
        description="添加时间,字符串类型JS格式化为yyyy-MM-dd hh:mm:ss,未精确到时间可传入00:00:00"
    )
    update_datetime: Optional[str] = Field(
        None,
        description="更新时间,字符串类型JS格式化为yyyy-MM-dd hh:mm:ss,未精确到时间可传入00:00:00"
    )


class BaseQueryRequest(BaseModel):
    """
    基础查询请求对象
    """
    add_datetime_desc: Optional[bool] = Field(
        None,
        description="添加时间倒序排序标志"
    )
    add_datetime_asc: Optional[bool] = Field(
        None,
        description="添加时间正序排序标志"
    )
    update_datetime_desc: Optional[bool] = Field(
        None,
        description="更新时间倒序排序标志"
    )
    update_datetime_asc: Optional[bool] = Field(
        None,
        description="更新时间正序排序标志"
    )
    remarks_desc: Optional[bool] = Field(
        None,
        description="备注倒序排序标志"
    )
    remarks_asc: Optional[bool] = Field(
        None,
        description="备注正序排序标志"
    )
    add_datetime_start: Optional[str] = Field(
        None,
        description="添加时间查询条件开始值,字符串类型JS格式化为yyyy-MM-dd hh:mm:ss,未精确到时间可传入00:00:00"
    )
    add_datetime_end: Optional[str] = Field(
        None,
        description="添加时间查询条件结束值,字符串类型JS格式化为yyyy-MM-dd hh:mm:ss,未精确到时间可传入00:00:00"
    )
    update_datetime_start: Optional[str] = Field(
        None,
        description="更新时间查询条件开始值,字符串类型JS格式化为yyyy-MM-dd hh:mm:ss,未精确到时间可传入00:00:00"
    )
    update_datetime_end: Optional[str] = Field(
        None,
        description="更新时间查询条件结束值,字符串类型JS格式化为yyyy-MM-dd hh:mm:ss,未精确到时间可传入00:00:00"
    )
    page: Optional[int] = Field(
        1,
        description="分页查询条件当前页数,传入值为-1时表示不进行分页，查询所有"
    )
    limit: Optional[int] = Field(
        10,
        description="分页查询条件结果限制条数,页数为-1时返回所有符合查询结果值，该值无效"
    )


class AuthBaseRequest(BaseRequest):
    """
    权限请求对象(增、删、改用)
    """
    name: Optional[str] = Field(
        None,
        description="权限的名称"
    )
    url: Optional[str] = Field(
        None,
        description="权限的请求路径"
    )
    status: Optional[bool] = Field(
        None,
        description="权限的使用状态, 0为禁用，1为启用"
    )


class AuthQueryRequest(BaseQueryRequest, AuthBaseRequest):
    """
    权限查询请求对象
    """
    name_like: Optional[str] = Field(
        None,
        description="权限查询，权限名称模糊匹配值"
    )
    url_like: Optional[str] = Field(
        None,
        description="权限查询，权限路径模糊匹配值"
    )
    name_desc: Optional[bool] = Field(
        None,
        description="权限查询，权限名称倒序排序标志"
    )
    name_asc: Optional[bool] = Field(
        None,
        description="权限查询，权限名称正序排序标志"
    )
    url_desc: Optional[bool] = Field(
        None,
        description="权限查询，权限路径倒序排序标志"
    )
    url_asc: Optional[bool] = Field(
        None,
        description="权限查询，权限路径正序排序标志"
    )
    status_desc: Optional[bool] = Field(
        None,
        description="权限查询，权限使用状态倒序排序标志"
    )
    status_asc: Optional[bool] = Field(
        None,
        description="权限查询，权限使用状态正序排序标志"
    )


class RoleBaseRequest(BaseRequest):
    """
    角色请求对象(增、删、改用)
    """
    auth_ids: Optional[List[str]] = Field(
        None,
        description="权限id集合,添加角色时与权限进行关联使用"
    )
    name: Optional[str] = Field(
        None,
        description="角色名称"
    )
    status: Optional[bool] = Field(
        None,
        description="角色使用状态，0为禁用，1为启用"
    )


class RoleQueryRequest(BaseQueryRequest, RoleBaseRequest):
    """
    角色查询请求对象
    """
    name_like: Optional[str] = Field(
        None,
        description="角色查询条件，角色名称模糊匹配关键字"
    )
    name_desc: Optional[bool] = Field(
        None,
        description="角色查询条件，角色名称倒序排序标志"
    )
    name_asc: Optional[bool] = Field(
        None,
        description="角色查询条件，角色名称正序排序标志"
    )
    status_desc: Optional[bool] = Field(
        None,
        description="角色查询条件，角色使用状态倒序排序标志"
    )
    status_asc: Optional[bool] = Field(
        None,
        description="角色查询条件，角色使用状态正序排序标志"
    )


class LoginRequest(BaseModel):
    """
    登陆请求对象
    """
    username: str
    pwd: str


class UserBaseRequest(BaseRequest):
    """
    用户请求对象(增、删、改用)
    """
    name: Optional[str] = Field(
        None,
        description="用户账号"
    )
    pwd: Optional[str] = Field(
        None,
        description="用户账号密码"
    )
    phone: Optional[str] = Field(
        None,
        description="管理员手机号"
    )
    email: Optional[str] = Field(
        None,
        description="管理员邮箱"
    )
    avatar: Optional[str] = Field(
        None,
        description="用户头像地址"
    )
    status: Optional[bool] = Field(
        None,
        description="用户使用状态"
    )


class UserQueryRequest(BaseQueryRequest, UserBaseRequest):
    """
    用户查询请求对象
    """
    name_like: Optional[str] = Field(
        None,
        description="用户账号查询条件，模糊匹配关键字"
    )
    name_desc: Optional[bool] = Field(
        None,
        description="用户账号查询条件，账号倒序排序标志"
    )
    name_asc: Optional[bool] = Field(
        None,
        description="用户账号查询条件，账号正序排序标志"
    )
    status_desc: Optional[bool] = Field(
        None,
        description="用户使用状态查询条件，使用状态倒序排序标志"
    )
    status_asc: Optional[bool] = Field(
        None,
        description="用户使用状态查询条件，使用状态正序排序标志"
    )


class AdminBaseRequest(BaseRequest):
    """
    管理员请求对象(增、删、改用)
    """
    role_id: Optional[str] = Field(
        None,
        description="管理员角色id"
    )
    name: Optional[str] = Field(
        None,
        description="管理员账号"
    )
    pwd: Optional[str] = Field(
        None,
        description="管理员账号密码"
    )
    phone: Optional[str] = Field(
        None,
        description="管理员手机号"
    )
    email: Optional[str] = Field(
        None,
        description="管理员邮箱"
    )
    avatar: Optional[str] = Field(
        None,
        description="管理员头像地址"
    )
    status: Optional[bool] = Field(
        None,
        description="管理员使用状态"
    )


class AdminQueryRequest(BaseQueryRequest, AdminBaseRequest):
    """
    管理员查询请求对象
    """
    name_like: Optional[str] = Field(
        None,
        description="管理员账号查询条件，模糊匹配关键字"
    )
    name_desc: Optional[bool] = Field(
        None,
        description="管理员账号查询条件，账号倒序排序标志"
    )
    name_asc: Optional[bool] = Field(
        None,
        description="管理员账号查询条件，账号正序排序标志"
    )
    status_desc: Optional[bool] = Field(
        None,
        description="管理员使用状态查询条件，使用状态倒序排序标志"
    )
    status_asc: Optional[bool] = Field(
        None,
        description="管理员使用状态查询条件，使用状态正序排序标志"
    )


class LoginLogBaseRequest(BaseRequest):
    """
    登录日志请求对象(增、删、改用)
    """
    user_id: str = Field(
        None,
        description="用户id，添加登录日志信息关联用户id使用"
    )
    ip: Optional[str] = Field(
        None,
        description="登录ip"
    )
    ua: Optional[str] = Field(
        None,
        description="登录ua"
    )


class LoginLogQueryRequest(BaseQueryRequest, LoginLogBaseRequest):
    """
    登录日志查询请求对象
    """
    ip_like: Optional[str] = Field(
        None,
        description="登录日志ip查询条件，模糊匹配关键字"
    )
    ua_like: Optional[str] = Field(
        None,
        description="登录日志ua查询条件，模糊匹配关键字"
    )
    ip_desc: Optional[bool] = Field(
        None,
        description="登录日志ip查询条件，ip排序倒序标志"
    )
    ip_asc: Optional[bool] = Field(
        None,
        description="登录日志ip查询条件，ip排序正序标志"
    )
    ua_desc: Optional[bool] = Field(
        None,
        description="登录日志ua查询条件，ua排序倒序标志"
    )
    ua_asc: Optional[bool] = Field(
        None,
        description="登录日志ua查询条件，ua排序正序标志"
    )
    user_id_desc: Optional[bool] = Field(
        None,
        description="登录日志记录用户查询条件，用户id排序倒序标志"
    )
    user_id_asc: Optional[bool] = Field(
        None,
        description="登录日志记录用户查询条件，用户id排序正序标志"
    )


class AdminLoginLogBaseRequest(BaseRequest):
    """
    登录日志请求对象(增、删、改用)
    """
    admin_id: str = Field(
        None,
        description="管理员id，添加登录日志信息关联用户id使用"
    )
    ip: Optional[str] = Field(
        None,
        description="登录ip"
    )
    ua: Optional[str] = Field(
        None,
        description="登录ua"
    )


class AdminLoginLogQueryRequest(BaseQueryRequest, AdminLoginLogBaseRequest):
    """
    登录日志查询请求对象
    """
    ip_like: Optional[str] = Field(
        None,
        description="登录日志ip查询条件，模糊匹配关键字"
    )
    ua_like: Optional[str] = Field(
        None,
        description="登录日志ua查询条件，模糊匹配关键字"
    )
    ip_desc: Optional[bool] = Field(
        None,
        description="登录日志ip查询条件，ip排序倒序标志"
    )
    ip_asc: Optional[bool] = Field(
        None,
        description="登录日志ip查询条件，ip排序正序标志"
    )
    ua_desc: Optional[bool] = Field(
        None,
        description="登录日志ua查询条件，ua排序倒序标志"
    )
    ua_asc: Optional[bool] = Field(
        None,
        description="登录日志ua查询条件，ua排序正序标志"
    )
    admin_id_desc: Optional[bool] = Field(
        None,
        description="登录日志记录管理员查询条件，管理员id排序倒序标志"
    )
    admin_id_asc: Optional[bool] = Field(
        None,
        description="登录日志记录管理员查询条件，管理员id排序正序标志"
    )


class OpLogBaseRequest(BaseRequest):
    """
    操作日志请求对象(增、删、改用)
    """
    user_id: str = Field(
        None,
        description="操作日志用户id，用以管理操作的用户"
    )
    op_type: int = Field(
        None,
        description="操作类型，0 增加 1 删 2 改 3 查"
    )
    content: str = Field(
        None,
        description="操作内容，执行操作的sql"
    )
    model: str = Field(
        None,
        description="执行操作对应的模块，根据调用对应的api来定"
    )


class OpLogQueryRequest(BaseQueryRequest, OpLogBaseRequest):
    """
    操作日志查询请求对象
    """
    content_like: Optional[str] = Field(
        None,
        description="操作日志内容查询条件，模糊匹配操作日志内容关键字"
    )
    model_like: Optional[str] = Field(
        None,
        description="操作日志模块名称查询条件，模糊匹配操作模块名称关键字"
    )
    op_type_desc: Optional[bool] = Field(
        None,
        description="操作类型查询条件，操作类型排序倒序标志"
    )
    op_type_asc: Optional[bool] = Field(
        None,
        description="操作类型查询条件，操作类型排序正序标志"
    )
    content_desc: Optional[bool] = Field(
        None,
        description="操作日志内容查询条件，操作日志内容排序倒序标志"
    )
    content_asc: Optional[bool] = Field(
        None,
        description='操作日志内容查询条件，操作日志内容正序排序标志'
    )
    model_desc: Optional[bool] = Field(
        None,
        description="操作日志模块名称查询条件，操作日志模块名称倒序排序标志"
    )
    model_asc: Optional[bool] = Field(
        None,
        description="操作日志模块名称查询条件，操作日志模块名称正序排序标志"
    )
    user_id_desc: Optional[bool] = Field(
        None,
        description="操作日志记录用户查询条件，用户id排序倒序标志"
    )
    user_id_asc: Optional[bool] = Field(
        None,
        description="操作日志记录用户查询条件，用户id排序正序标志"
    )


class AdCodeBaseRequest(BaseRequest):
    province_name: Optional[str] = Field(
        None,
        description="省份名称"
    )
    city_name: Optional[str] = Field(
        None,
        description="城市名称"
    )
    city_code: Optional[str] = Field(
        None,
        description="城市代码"
    )
    area_name: Optional[str] = Field(
        None,
        description="地区名称"
    )
    area_code: Optional[str] = Field(
        None,
        description="地区代码"
    )
    street_name: Optional[str] = Field(
        None,
        description="街道名称"
    )
    street_code: Optional[str] = Field(
        None,
        description="街道代码"
    )


class AdCodeQueryRequest(AdCodeBaseRequest):
    province_name_like: Optional[str] = Field(
        None,
        description="省份名称模糊匹配"
    )
    city_name_like: Optional[str] = Field(
        None,
        description="城市名称模糊匹配"
    )
    area_name_like: Optional[str] = Field(
        None,
        description="地区名称模糊匹配"
    )
    street_name_like: Optional[str] = Field(
        None,
        description="街道名称模糊匹配"
    )
    province_code_desc: Optional[bool] = Field(
        None,
        description="省份代码倒序排序"
    )
    province_code_asc: Optional[bool] = Field(
        None,
        description="省份代码正序排序"
    )
    province_name_desc: Optional[bool] = Field(
        None,
        description="省份名称倒序排序"
    )
    province_name_asc: Optional[bool] = Field(
        None,
        description="省份名称正序排序"
    )
    city_code_desc: Optional[bool] = Field(
        None,
        description="城市代码倒序排序"
    )
    city_code_asc: Optional[bool] = Field(
        None,
        description="城市代码正序排序"
    )
    city_name_desc: Optional[bool] = Field(
        None,
        description="城市名称倒序排序"
    )
    city_name_asc: Optional[bool] = Field(
        None,
        description="城市名称正序排序"
    )
    area_code_desc: Optional[bool] = Field(
        None,
        description="地区代码倒序排序"
    )
    area_code_asc: Optional[bool] = Field(
        None,
        description="地区代码正序排序"
    )
    area_name_desc: Optional[bool] = Field(
        None,
        description="地区名称倒序排序"
    )
    area_name_asc: Optional[bool] = Field(
        None,
        description="地区名称正序排序"
    )
    street_code_desc: Optional[bool] = Field(
        None,
        description="街道代码倒序排序"
    )
    street_code_asc: Optional[bool] = Field(
        None,
        description="街道代码正序排序"
    )
    street_name_desc: Optional[bool] = Field(
        None,
        description="街道名称倒序排序"
    )
    street_name_asc: Optional[bool] = Field(
        None,
        description="街道名称正序排序"
    )
    add_datetime_desc: Optional[bool] = Field(
        None,
        description="添加时间倒序排序"
    )
    add_datetime_asc: Optional[bool] = Field(
        None,
        description="添加时间正序排序"
    )
    update_datetime_desc: Optional[bool] = Field(
        None,
        description="更新时间倒序排序"
    )
    update_datetime_asc: Optional[bool] = Field(
        None,
        description="更新时间正序排序"
    )


# 获取查询条件dict时要排除的字段相关关键字
query_ignore_keys = ['_desc', '_asc', 'ids', 'auth_ids', 'page', 'limit']


def get_query_params(**kwargs):
    """
    根据对象的实体类名及队形的属性列表获取对应的查询字典
    :param kwargs:
    :return:
    """
    query_params = {}
    for v in kwargs['props']:
        for j in query_ignore_keys:
            if j in v:
                break
        else:
            # 范围查询开始
            if '_start' in v:
                # 日期类型字段
                if 'datetime' in v:
                    query_params[v] = "%s.%s >= datetime.datetime.strptime(request_param.%s, '%s')" % (
                        kwargs['model_name'], v.split('_start')[0], v, '%Y-%m-%d %H:%M:%S')
                else:
                    query_params[v] = "%s.%s >= request_param.%s" % (
                        kwargs['model_name'], v.split('_start')[0], v)
            # 范围查询借宿
            elif '_end' in v:
                # 日期类型字段
                if 'datetime' in v:
                    query_params[v] = "%s.%s <= datetime.datetime.strptime(request_param.%s, '%s')" % (
                        kwargs['model_name'], v.split('_end')[0], v, '%Y-%m-%d %H:%M:%S')
                else:
                    query_params[v] = "%s.%s <= request_param.%s" % (
                        kwargs['model_name'], v.split('_end')[0], v)
            # 模糊查询
            elif '_like' in v:
                query_params[v] = "%s.%s ** ('%s' + request_param.%s + '%s')" % (
                    kwargs['model_name'], v.split('_like')[0], '%', v, '%')
            # 精准查询
            else:
                query_params[v] = "%s.%s == request_param.%s" % (kwargs['model_name'], v, v)
    return query_params


def get_sort_params(**kwargs):
    """
    根据对象的实体类名及对应的属性列表获取对应的排序字典
    :param kwargs:
    :return:
    """
    sort_params = {}
    for v in kwargs['props']:
        if '_desc' in v:
            sort_params[v] = '%s.%s.desc()' % (kwargs['model_name'], v.split('_desc')[0])
        elif '_asc' in v:
            sort_params[v] = '%s.%s.asc()' % (kwargs['model_name'], v.split('_asc')[0])

    return sort_params


if __name__ == '__main__':
    print(BaseQueryRequest.__fields__.keys())
