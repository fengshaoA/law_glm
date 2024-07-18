from pydantic import BaseModel, Field
from enum import Enum

class AddressInfo(BaseModel):
    地址 :str
    省份 :str
    城市:str
    区县 :str


class AddressCode(BaseModel):
    省份 :str
    城市 :str
    城市区划代码 :str
    区县 :str
    区县区划代码 :str

def build_enum_class(dataclass, exclude_enums=[]):
    keys = [key for key in dataclass.__fields__.keys() if key not in exclude_enums]
    return Enum(dataclass.__name__ + "Enum", dict(zip(keys, keys)))


AddressInfoEnum = build_enum_class(AddressInfo,exclude_enums=['详细地址'])
AddressCodeEnum = build_enum_class(AddressCode,exclude_enums=['省市区县'])

def build_enum_list(enum_class): return [enum.value for enum in enum_class]


address_schema = f"""
详细地址对应的省份城市区县信息（AddressInfo）有下列字段：
{build_enum_list(AddressInfoEnum)}
------------------------------------------------
根据省市区查询区划代码信息（AddressCode）有下列字段：
{build_enum_list(AddressCodeEnum)}
------------------------------------------------
"""