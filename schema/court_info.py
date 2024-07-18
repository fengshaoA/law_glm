from pydantic import BaseModel, Field
from enum import Enum

class CourtInfo(BaseModel):
    法院名称 :str
    法院负责人:str
    成立日期:str
    法院地址:str
    法院联系电话 :str
    法院官网 :str


class CourtCode(BaseModel):
    法院名称 :str
    行政级别 :str
    法院级别 :str
    法院代字 :str
    区划代码 :str
    级别 :str


def build_enum_class(dataclass, exclude_enums=[]):
    keys = [key for key in dataclass.__fields__.keys() if key not in exclude_enums]
    return Enum(dataclass.__name__ + "Enum", dict(zip(keys, keys)))


CourtInfoEnum = build_enum_class(CourtInfo,exclude_enums=['法院名称'])
CourtCodeEnum = build_enum_class(CourtCode,exclude_enums=['法院名称或者法院代字'])


def build_enum_list(enum_class): return [enum.value for enum in enum_class]

court_schema = f"""
# 根据法院名称查询法院名录相关信息（CourtInfo）有下列字段：
{build_enum_list(CourtInfoEnum)}
------------------------------------------------

根据法院名称或者法院代字查询法院代字等相关数据(CourtCode)有下列字段：
{build_enum_list(CourtCodeEnum)}
------------------------------------------------
"""
