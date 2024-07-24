from pydantic import BaseModel, Field
from enum import Enum

class LegalDoc(BaseModel):
    关联公司 :str
    标题 :str
    案号 :str
    文书类型 :str
    原告 :str
    被告 :str
    原告律师事务所 :str
    被告律师事务所 :str
    案由 :str
    涉案金额 :str
    判决结果 :str
    日期 :str
    文件名 :str


def build_enum_class(dataclass, exclude_enums=[]):
    keys = [key for key in dataclass.__fields__.keys() if key not in exclude_enums]
    return Enum(dataclass.__name__ + "Enum", dict(zip(keys, keys)))


LegalDocumentEnum = build_enum_class(LegalDoc, exclude_enums=["案号"])

def build_enum_list(enum_class): return [enum.value for enum in enum_class]

legal_schema = f"""
公司法律文书表（LegalDocument）有下列字段：
{build_enum_list(LegalDocumentEnum)}
------------------------------------------------
"""