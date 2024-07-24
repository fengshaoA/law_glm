import requests
from register.tool_register import register_tool, get_tools, dispatch_tool
from typing import get_origin, Annotated, Union, List, Optional
from schema.legal_info import  LegalDoc,LegalDocumentEnum


api_list = [
    "get_legal_document",
    "get_legal_document_list",
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


# Tool Definitions
def http_api_call_v2(api_name, data, max_data_len=None):
    url = f"{domain}/law_api/s1_b/{api_name}"

    # data = {"company_name": company_name, "years": years, "is_plaintiff": is_plaintiff, "max_amount": max_amount,
    #         "min_amount": min_amount}
    company_name = data['company_name'] if 'company_name' in data else ''
    years = data['years'] if 'years' in data else ""
    is_plaintiff = data['is_plaintiff'] if "is_plaintiff" in data else ""
    max_amount = 1000000000000
    min_amount = -100
    if 'max_amount' in data:
        max_amount = float(data['max_amount'])
    if 'min_amount' in data:
        min_amount = float(data['min_amount'])

    target_data = {"query_conds": {"关联公司": company_name}, "need_fields": []}
    rsp = requests.post(url, json=target_data, headers=headers)

    final_rsp = rsp.json()
    final_rsp = [final_rsp] if isinstance(final_rsp, dict) else final_rsp
    if 'Error' in final_rsp or len(final_rsp) == 0:
        return {"return_items_count": len(final_rsp), "return": [{"公司名称": ""}]}

    if is_plaintiff != "":
        is_plaintiff = 0 if str(is_plaintiff).lower() == 'no' else 1
    else:
        is_plaintiff == ""
    if max_amount == "" or max_amount == None:
        max_amount = 100000000000
    if min_amount == "" or min_amount == None:
        min_amount = -1000
    ret = list()
    for items in final_rsp:
        case_code = str(items['案号']).replace('（', '(').replace('）', ')')
        case_years = str(case_code.split(')')[0]).split('(')[1]
        if years != "":
            if case_years == years:
                if is_plaintiff != "":
                    if is_plaintiff:
                        if items['原告'] == company_name or company_name in items['原告']:
                            if float(items['涉案金额']) >= min_amount and float(items["涉案金额"]) <= max_amount:
                                ret.append(items)
                    else:
                        if items['被告'] == company_name or company_name in items['被告']:
                            if float(items['涉案金额']) >= min_amount and float(items["涉案金额"]) <= max_amount:
                                ret.append(items)
                else:
                    if float(items['涉案金额']) >= min_amount and float(items["涉案金额"]) <= max_amount:
                        ret.append(items)
        else:
            if is_plaintiff != "":
                if is_plaintiff:
                    if items['原告'] == company_name or company_name in items['原告']:
                        if float(items['涉案金额']) >= min_amount and float(items["涉案金额"]) <= max_amount:
                            ret.append(items)
                else:
                    if items['被告'] == company_name or company_name in items['被告']:
                        if float(items['涉案金额']) >= min_amount and float(items["涉案金额"]) <= max_amount:
                            ret.append(items)
            else:
                if float(items['涉案金额']) >= min_amount and float(items["涉案金额"]) <= max_amount:
                    ret.append(items)

    final_rsp = [ret] if isinstance(ret, dict) else ret

    if max_data_len is None:
        max_data_len = len(final_rsp)
    return {
        "return_items_count": len(final_rsp),
        "return": final_rsp[:max_data_len],
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
def get_legal_document(
        case_num: Annotated[str, "案号", True],
) -> LegalDoc:
    """
    公司法律文书类工具
    根据案号查询相关法律文书的内容，
    """
    if isinstance(case_num, str):
        case_num = case_num.replace('（', '(').replace('）', ')').replace('【','(').replace('】',')').replace('[','(').replace(']',')')
    return http_api_call("get_legal_document",  {"query_conds":{"案号": case_num},"need_fields":[]})

@register_tool
def get_legal_document_list(company_name:Annotated[str,"公司名称",True]) -> List[LegalDoc]:
    """
    公司法律文书类工具
    根据公司名称查询公司所有法律文书信息列表，不做任何条件过滤
    """
    company_name = augment_company_name(company_name)[0]

    return http_api_call("get_legal_document_list",{"query_conds":{"关联公司": company_name},"need_fields":[]})




@register_tool
def years_with_legal_doc(
        company_name: Annotated[str, "公司名称", True],
        years: Annotated[str, "年份", True],
        is_plaintiff:Annotated[str,"是否是原告",True]
) -> List[LegalDoc]:
    """
    公司法律文书类工具
    从公司涉案列表中获取指定年份{years},公司作为原告还是被告{is_plaintiff}的法律文书信息
    """

    data = {"company_name":company_name,"years":years,"is_plaintiff":is_plaintiff}

    return http_api_call_v2("get_legal_document_list", data, max_data_len=None)

@register_tool
def max_min_amount_with_legal_doc(
        company_name: Annotated[str, "公司名称", True],
        is_plaintiff:Annotated[str,"原告的话Yes被告的话No",True],
        max_amount:Annotated[str,"最大涉案金额",True],
        min_amount:Annotated[str,"最小涉案金额",True]
) -> List[LegalDoc]:
    """
    公司法律文书类工具
    从公司涉案列表中获取公司作为原告或者被告{is_plaintiff}，涉案金额在最大值{max_amount}最小值{min_amount}之间的法律文书信息
    """

    data = {"company_name":company_name,"is_plaintiff":is_plaintiff,"max_amount":max_amount,"min_amount":min_amount}

    return http_api_call_v2("get_legal_document_list", data, max_data_len=None)

@register_tool
def plaintiff_with_legal_doc(
        company_name: Annotated[str, "公司名称", True],
        is_plaintiff:Annotated[str,"原告的话Yes被告的话No",True],
) -> List[LegalDoc]:
    """
    公司法律文书类工具
    从公司涉案列表中获取公司作为原告或者被告{is_plaintiff}的法律文书信息
    """

    data = {"company_name":company_name,"is_plaintiff":is_plaintiff}

    return http_api_call_v2("get_legal_document_list", data, max_data_len=None)
