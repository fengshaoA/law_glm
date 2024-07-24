import requests
from register.tool_register import register_tool, get_tools, dispatch_tool
from typing import get_origin, Annotated, Union, List, Optional
from schema.company_info import CompanyInfo, SubCompanyInfo,CompanyRegister,CompanyInfoEnum,SubCompanyInfoEnum,CompanyRegisterEnum

api_list = [
    "get_company_info",
    "get_company_register",
    "get_company_register_name",
    "get_sub_company_info",
    "get_sub_company_info_list",

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
def get_company_name(company_info:Annotated[str,"公司名称或者公司简称或者公司代码或者股票代码或者社会统一信用代码等信息",True],)->str:
    """
    公司类工具
    根据公司名称、公司简称、公司代码(股票代码)或者社会统一信用代码等信息获得公司名称
    """
    ret = augment_company_name(company_info)
    return {"公司名称":ret[0]}

@register_tool
def get_company_info(
        company_name: Annotated[str, "公司名称", True],
) -> CompanyInfo:
    """
    公司类工具
    根据上市公司名称获得该公司所有基本信息
    """
    company_name = augment_company_name(company_name)[0]
    return http_api_call("get_company_info", {"query_conds":{"公司名称": company_name},"need_fields":[]})


@register_tool
def get_company_register(
        company_name: Annotated[str, "公司名称", True],
) -> CompanyRegister:
    """
    公司类工具
    根据未上市公司名称（公名称应该是公司全称）获得该公司所有注册信息
    """
    company_name = augment_company_name(company_name)[0]
    return http_api_call("get_company_register", {"query_conds":{"公司名称": company_name},"need_fields":[]})



@register_tool
def get_parent_company_info(
        company_name: Annotated[str, "子公司名称", True],
) -> SubCompanyInfo:
    """
    公司类工具
    根据公司名称获得母公司的公司名称、投资比例、投资金额等信息
    """
    company_name = augment_company_name(company_name)[0]
    resp = http_api_call("get_sub_company_info", {"query_conds":{"公司名称": company_name},"need_fields":[]})

    parent_company = resp['return'][0]['关联上市公司全称']
    sub_company = resp['return'][0]['公司名称']
    resp['return'][0]['母公司名称'] = parent_company
    resp['return'][0]['子公司名称'] = sub_company
    return resp

@register_tool
def get_sub_company_info_list(
        company_name: Annotated[str, "母公司名称", True],
) -> List[SubCompanyInfo]:
    """
    公司类工具
    根据上市公司（母公司）的名称查询该公司投资的所有子公司信息list
    """
    company_name = augment_company_name(company_name)[0]
    resp = http_api_call("get_sub_company_info_list", {"query_conds":{"关联上市公司全称": company_name},"need_fields":[]})
    ret = resp['return']
    for i in range(len(ret)):
        parent_company = ret[i]['关联上市公司全称']
        sub_company = ret[i]['公司名称']
        ret[i]['母公司名称'] = parent_company
        ret[i]['子公司名称'] = sub_company

    resp['return'] = ret

    return resp


@register_tool
def get_max_invested_sub_company_info(
        company_name: Annotated[str, "母公司名称", True],
) -> List[SubCompanyInfo]:
    """
    公司类工具
    根据上市公司（母公司）的名称获取该公司投资金额最高的子公司信息
    """
    company_name = augment_company_name(company_name)[0]
    resp = http_api_call("get_sub_company_info_list", {"query_conds":{"公司名称": company_name},"need_fields":[]})
    ret = resp['return']
    for i in range(len(ret)):
        parent_company = ret['return'][i]['关联上市公司全称']
        sub_company = ret['return'][i]['公司名称']
        ret['return'][i]['母公司名称'] = parent_company
        ret['return'][i]['子公司名称'] = sub_company

    resp['return'] = ret

    return resp