from pydantic import BaseModel, Field
from enum import Enum

class WeatherInfo(BaseModel):
    日期 :str
    省份 :str
    城市 :str
    天气 :str
    最高温度 :str
    最低温度 :str
    湿度 :str


def build_enum_class(dataclass, exclude_enums=[]):
    keys = [key for key in dataclass.__fields__.keys() if key not in exclude_enums]
    return Enum(dataclass.__name__ + "Enum", dict(zip(keys, keys)))

WeatherInfoEnum = build_enum_class(WeatherInfo,exclude_enums=['省市日期'])

def build_enum_list(enum_class): return [enum.value for enum in enum_class]

lawfirm_schema = f"""
根据日期及省份城市查询天气相关信息(WeatherInfo)有下列字段：
{build_enum_list(WeatherInfoEnum)}
------------------------------------------------
"""