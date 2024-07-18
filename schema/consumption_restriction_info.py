from pydantic import BaseModel, Field
from enum import Enum

class ConsumptionRestrictionInfo(BaseModel):
    限制高消费企业名称:str
    案号 :str
    法定代表人 :str
    申请人 :str
    涉案金额 :str
    执行法院 :str
    立案日期 :str
    限高发布日期 :str


def build_enum_class(dataclass, exclude_enums=[]):
    keys = [key for key in dataclass.__fields__.keys() if key not in exclude_enums]
    return Enum(dataclass.__name__ + "Enum", dict(zip(keys, keys)))


ConsumptionRestrictionInfoEnum = build_enum_class(ConsumptionRestrictionInfo,exclude_enums=['案号'])

def build_enum_list(enum_class): return [enum.value for enum in enum_class]

consumptionrestriction_schema = f"""
公司限制高消费相关信息（ConsumptionRestrictionInfo）有下列字段：
{build_enum_list(ConsumptionRestrictionInfoEnum)}
------------------------------------------------
"""