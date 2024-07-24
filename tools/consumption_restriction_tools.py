import requests
from register.tool_register import register_tool, get_tools, dispatch_tool
from typing import get_origin, Annotated, Union, List, Optional
from schema.consumption_restriction_info import ConsumptionRestrictionInfo,ConsumptionRestrictionInfoEnum

api_list = [
    "get_xzgxf_info_list",
    "get_xzgxf_info",
]

domain = "https://comm.chatglm.cn"

headers = {
    'Content-Type': 'application/json',
    "Authorization": "Bearer 95D4B27F35E304586FDCACE72F51FF9D9A77382112F16F11"
}


# Tool Definitions
def http_api_call(api_name, data, max_data_len=None):
    url = f"{domain}/law_api/s1_b/{api_name}"

    rsp = requests.post(url, json=data, headers=headers)

    final_rsp = rsp.json()
    if 'Error' in final_rsp or len(final_rsp) == 0:
        return {"return_items_count": len(final_rsp), "return": [{'公司名称': ""}]}

    final_rsp = [final_rsp] if isinstance(final_rsp, dict) else final_rsp

    if max_data_len is None:
        max_data_len = len(final_rsp)
    return {
        "return_items_count": len(final_rsp),
        "return": final_rsp[:max_data_len]
    }

def get_company_name_by_bref(bref):
    """根据公司简称获得公司名称"""
    company_names = http_api_call("get_company_info", {"query_conds":{"公司简称": bref},"need_fields":[]})["return"][0]['公司名称']
    return company_names


def get_company_name_by_com_code(company_code):
    """根据公司代码（股票代码）查询公司名称"""
    company_names = http_api_call("get_company_info", {"query_conds":{"公司代码": company_code},"need_fields":[]})["return"][0]["公司名称"]
    return company_names

def get_company_name_by_credit_code(unified_social_credit_code):
    """根据社会统一信用代码查询公司名称"""
    company_names = http_api_call("get_company_register_name", {"query_conds": {"统一社会信用代码": unified_social_credit_code}, "need_fields": []})['return'][0]["公司名称"]

    return company_names



def augment_company_name(company_name):
    ret_list = list()
    company_name = company_name if isinstance(company_name, list) else [company_name]
    for c in company_name[:]:
        ret = get_company_name_by_bref(c)
        if ret != "":
            ret_list.append(ret)
        ret = get_company_name_by_com_code(c)
        if ret != "":
            ret_list.append(ret)
        ret = get_company_name_by_credit_code(c)
        if ret != "":
            ret_list.append(ret)

    ret = list(set(ret_list))
    if len(ret) == 0:
        ret.append(company_name[0])

    return ret


@register_tool
def case_num_with_consumption_restriction_info(
        case_num:Annotated[str,"案号",True]
)-> ConsumptionRestrictionInfo:
    """
    公司法律文书类工具
    根据案号查询限制高消费相关信息
    """
    if isinstance(case_num, str):
        case_num = case_num.replace('(', '（').replace(')', '）').replace('【','（').replace('】','）').replace('[','（').replace(']','）')
    return http_api_call("get_xzgxf_info",{"query_conds":{"案号": case_num},"need_fields":[]})

@register_tool
def company_name_with_consumption_restriction_info(
        company_name:Annotated[str,'公司名称或者企业名称',True]
)->List[ConsumptionRestrictionInfo]:
    """
    公司法律文书类工具
    根据公司名称或者企业名称查询该公司所有限制高消费相关信息list
    """
    company_name = augment_company_name(company_name)[0]
    return http_api_call("get_xzgxf_info_list",{"query_conds":{"限制高消费企业名称": company_name},"need_fields":[]})
