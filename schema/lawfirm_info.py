from pydantic import BaseModel, Field
from enum import Enum

class LawfirmInfo(BaseModel):
    律师事务所名称 :str
    律师事务所唯一编码 :str
    律师事务所负责人  :str
    事务所注册资本 :str
    事务所成立日期 :str
    律师事务所地址 :str
    通讯电话 :str
    通讯邮箱 :str
    律所登记机关 :str


class LawfirmLog(BaseModel):
    律师事务所名称 :str
    业务量排名 :str
    服务已上市公司 :str
    报告期间所服务上市公司违规事件 :str
    报告期所服务上市公司接受立案调查 :str


def build_enum_class(dataclass, exclude_enums=[]):
    keys = [key for key in dataclass.__fields__.keys() if key not in exclude_enums]
    return Enum(dataclass.__name__ + "Enum", dict(zip(keys, keys)))

LawfirmInfoEnum = build_enum_class(LawfirmInfo,exclude_enums=['律师事务所名称'])
LawfirmLogEnum = build_enum_class(LawfirmLog,exclude_enums=['律师事务所名称'])

def build_enum_list(enum_class): return [enum.value for enum in enum_class]

lawfirm_schema = f"""
根据律师事务所查询律师事务所名录(LawfirmInfo)有下列字段：
{build_enum_list(LawfirmInfoEnum)}
------------------------------------------------

根据律师事务所查询律师事务所统计数据(LawfirmLog)有下列字段：
{build_enum_list(LawfirmLogEnum)}
------------------------------------------------
"""