import requests
from tool_register.tool_register import register_tool, get_tools, dispatch_tool
from typing import get_origin, Annotated, Union, List, Optional


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
def citizens_sue_citizens_civil_complaint(
        plaintiff_name: Annotated[str, "原告人名称或者原告公司名称或者原告公司法人", True],
        defendant_name: Annotated[str, "被告人名称或者被告公司名称或者被告公司法人", True],
        plaintiff_lawfirm_name: Annotated[str, "原告律师事务所名称", True],
        defendant_lawfirm_name: Annotated[str, "被告律师事务所名称", True],
        dates: Annotated[str, "申诉日期", True],
        cause: Annotated[str, "上诉原因", True],
        court_name: Annotated[str, "上诉法院", True]) -> str:
    """
    公民起诉公民或者公司法人起诉公司法人
    通过原告个人或者原告法人，被告个人或者被告法人，原告辩护律师事务所，被告辩护律师事务所，诉讼时间，诉讼原因，受理法院等信息来生成一份民事诉讼状给受理法院
    例如：
    深圳市佳士科技股份有限公司的法人与天津凯发电气股份有限公司的法人发生了产品生产者责任纠纷
    问题中出现 深圳市佳士科技股份有限公司的法人 与 天津凯发电气股份有限公司的法人 产生纠纷 则可以被判定为个人与个人产生纠纷

    """
    ret = {'原告': '-', '原告性别': '-', '原告生日': '-', '原告民族': '-', '原告工作单位': '-', '原告地址': '-', '原告联系方式': '-',
           '原告委托诉讼代理人': '-', '原告委托诉讼代理人联系方式': '-', '被告': '-', '被告性别': '-', '被告生日': '-', '被告民族': '-',
           '被告工作单位': '-', '被告地址': '-', '被告联系方式': '-', '被告委托诉讼代理人': '-', '被告委托诉讼代理人联系方式': '-',
           '诉讼请求': '-', '事实和理由': '上诉', '证据': 'PPPPP', '法院名称': '-', '起诉日期': '-'}

    # 获得原告个人的信息
    company_name = augment_company_name(plaintiff_name)[0]
    company_name2 = augment_company_name(defendant_name)[0]
    resp = http_api_call("get_company_info", {"query_conds": {"公司名称": company_name}, "need_fields": []})['return'][0]
    resp2 = http_api_call("get_company_info", {"query_conds": {"公司名称": company_name2}, "need_fields": []})['return'][0]

    lawfirm_resp = \
    http_api_call("get_lawfirm_info", {"query_conds": {"律师事务所名称": plaintiff_lawfirm_name}, "need_fields": []})[
        'return'][0]
    lawfirm_resp2 = \
    http_api_call("get_lawfirm_info", {"query_conds": {"律师事务所名称": defendant_lawfirm_name}, "need_fields": []})[
        'return'][0]

    if len(resp) > 0:
        ret['原告'] = resp['法人代表'] if "法人代表" in resp else ""
        ret['原告工作单位'] = company_name
        ret['原告地址'] = resp['办公地址'] if '办公地址' in resp else ""
        ret['原告联系方式'] = resp['联系电话'] if '联系电话' in resp else ""
    if len(lawfirm_resp) > 0:
        ret['原告委托诉讼代理人'] = plaintiff_lawfirm_name
        ret['原告委托诉讼代理人联系方式'] = lawfirm_resp['通讯电话'] if '通讯电话' in lawfirm_resp else ""

    if len(resp2) > 0:
        ret['被告'] = resp2['法人代表'] if "法人代表" in resp2 else ""
        ret['被告工作单位'] = company_name2
        ret['被告地址'] = resp2['办公地址'] if '办公地址' in resp2 else ""
        ret['被告联系方式'] = resp2['联系电话'] if '联系电话' in resp2 else ""
    if len(lawfirm_resp2) > 0:
        ret['被告委托诉讼代理人'] = defendant_lawfirm_name
        ret['被告委托诉讼代理人联系方式'] = lawfirm_resp2['通讯电话'] if '通讯电话' in lawfirm_resp2 else ""

    ret['诉讼请求'] = cause
    ret['起诉日期'] = dates
    ret['法院名称'] = court_name

    return http_api_call("get_citizens_sue_citizens", ret)


@register_tool
def citizens_sue_company_civil_complaint(plaintiff_name: Annotated[str, "原告人名称或者原告公司名称或者原告公司法人", True],
                                         defendant_name: Annotated[str, "被告人名称或者被告公司名称或者被告公司法人", True],
                                         plaintiff_lawfirm_name: Annotated[str, "原告律师事务所名称", True],
                                         defendant_lawfirm_name: Annotated[str, "被告律师事务所名称", True],
                                         dates: Annotated[str, "申诉日期", True],
                                         cause: Annotated[str, "上诉原因", True],
                                         court_name: Annotated[str, "上诉法院", True]) -> str:
    """
    个人起诉公司或者公司法人起诉公司
    通过原告个人或者原告公司法人，被告公司，原告辩护律师事务所，被告辩护律师事务所，诉讼时间，诉讼原因，受理法院等信息来生成一份民事诉讼状给受理法院
    例如：
    南京康尼机电股份有限公司法人与江苏江南高纤股份有限公司发生了民事纠纷
    问题中出现 南京康尼机电股份有限公司法人 与 江苏江南高纤股份有限公司 产生纠纷 则可以被判定为个人与公司产生纠纷
    """
    ret = {'原告': '-', '原告性别': '-', '原告生日': '-', '原告民族': '-', '原告工作单位': '-', '原告地址': '-', '原告联系方式': '-',
           '原告委托诉讼代理人': '-', '原告委托诉讼代理人联系方式': '-', '被告': '-', '被告地址': '-', '被告法定代表人': '-', '被告联系方式': '-',
           '被告委托诉讼代理人': '-', '被告委托诉讼代理人联系方式': '-', '诉讼请求': '-', '事实和理由': '上诉', '证据': 'PPPPP', '法院名称': '-', '起诉日期': '-'}

    # 获得原告个人的信息
    company_name = augment_company_name(plaintiff_name)[0]
    company_name2 = augment_company_name(defendant_name)[0]
    resp = http_api_call("get_company_info", {"query_conds": {"公司名称": company_name}, "need_fields": []})['return'][0]
    resp2 = http_api_call("get_company_info", {"query_conds": {"公司名称": company_name2}, "need_fields": []})['return'][0]

    lawfirm_resp = \
        http_api_call("get_lawfirm_info", {"query_conds": {"律师事务所名称": plaintiff_lawfirm_name}, "need_fields": []})[
            'return'][0]
    lawfirm_resp2 = \
        http_api_call("get_lawfirm_info", {"query_conds": {"律师事务所名称": defendant_lawfirm_name}, "need_fields": []})[
            'return'][0]

    if len(resp) > 0:
        ret['原告'] = resp['法人代表'] if "法人代表" in resp else ""
        ret['原告工作单位'] = company_name
        ret['原告地址'] = resp['办公地址'] if '办公地址' in resp else ""
        ret['原告联系方式'] = resp['联系电话'] if '联系电话' in resp else ""
    if len(lawfirm_resp) > 0:
        ret['原告委托诉讼代理人'] = plaintiff_lawfirm_name
        ret['原告委托诉讼代理人联系方式'] = lawfirm_resp['通讯电话'] if '通讯电话' in lawfirm_resp else ""

    if len(resp2) > 0:
        ret['被告'] = company_name2
        ret['被告地址'] = resp2['办公地址'] if '办公地址' in resp2 else ""
        ret['被告法定代表人'] = resp2['法人代表'] if "法人代表" in resp else ""
        ret['被告联系方式'] = resp2['联系电话'] if '联系电话' in resp2 else ""
    if len(lawfirm_resp2) > 0:
        ret['被告委托诉讼代理人'] = defendant_lawfirm_name
        ret['被告委托诉讼代理人联系方式'] = lawfirm_resp2['通讯电话'] if '通讯电话' in lawfirm_resp2 else ""

    ret['诉讼请求'] = cause
    ret['起诉日期'] = dates
    ret['法院名称'] = court_name

    return http_api_call("get_citizens_sue_company", ret)


@register_tool
def company_sue_company_civil_complaint(plaintiff_name: Annotated[str, "原告人名称或者原告公司名称或者原告公司法人", True],
                                        defendant_name: Annotated[str, "被告人名称或者被告公司名称或者被告公司法人", True],
                                        plaintiff_lawfirm_name: Annotated[str, "原告律师事务所名称", True],
                                        defendant_lawfirm_name: Annotated[str, "被告律师事务所名称", True],
                                        dates: Annotated[str, "申诉日期", True],
                                        cause: Annotated[str, "上诉原因", True],
                                        court_name: Annotated[str, "上诉法院", True]) -> str:
    """
    公司起诉公司
    通过原告公司，被告公司，原告辩护律师事务所，被告辩护律师事务所，诉讼时间，诉讼原因，受理法院等信息来生成一份民事诉讼状给受理法院
    例如：
    河北养元智汇饮品股份有限公司与通威股份有限公司发生了买卖合同纠纷，
    问题中出现 河北养元智汇饮品股份有限公司 与 通威股份有限公司 产生纠纷 则可以被判定为公司与公司产生纠纷
    """
    ret = {'原告': '-', '原告地址': '-', '原告法定代表人': '-', '原告联系方式': '-', '原告委托诉讼代理人': '-', '原告委托诉讼代理人联系方式': '-', '被告': '-',
           '被告地址': '-', '被告法定代表人': '-', '被告联系方式': '-', '被告委托诉讼代理人': '-', '被告委托诉讼代理人联系方式': '-', '诉讼请求': '-',
           '事实和理由': '上诉', '证据': 'PPPPP', '法院名称': '-', '起诉日期': '-'}
    # 获得原告个人的信息
    company_name = augment_company_name(plaintiff_name)[0]
    company_name2 = augment_company_name(defendant_name)[0]
    resp = http_api_call("get_company_info", {"query_conds": {"公司名称": company_name}, "need_fields": []})['return'][0]
    resp2 = http_api_call("get_company_info", {"query_conds": {"公司名称": company_name2}, "need_fields": []})['return'][0]

    lawfirm_resp = \
        http_api_call("get_lawfirm_info", {"query_conds": {"律师事务所名称": plaintiff_lawfirm_name}, "need_fields": []})[
            'return'][0]
    lawfirm_resp2 = \
        http_api_call("get_lawfirm_info", {"query_conds": {"律师事务所名称": defendant_lawfirm_name}, "need_fields": []})[
            'return'][0]

    if len(resp) > 0:
        ret['原告'] = company_name
        ret['原告地址'] = resp['办公地址'] if '办公地址' in resp else ""
        ret['原告法定代表人'] = resp['法人代表'] if "法人代表" in resp else ""
        ret['原告联系方式'] = resp['联系电话'] if '联系电话' in resp else ""
    if len(lawfirm_resp) > 0:
        ret['原告委托诉讼代理人'] = plaintiff_lawfirm_name
        ret['原告委托诉讼代理人联系方式'] = lawfirm_resp['通讯电话'] if '通讯电话' in lawfirm_resp else ""

    if len(resp2) > 0:
        ret['被告'] = company_name2
        ret['被告地址'] = resp2['办公地址'] if '办公地址' in resp2 else ""
        ret['被告法定代表人'] = resp2['法人代表'] if "法人代表" in resp else ""
        ret['被告联系方式'] = resp2['联系电话'] if '联系电话' in resp2 else ""
    if len(lawfirm_resp2) > 0:
        ret['被告委托诉讼代理人'] = defendant_lawfirm_name
        ret['被告委托诉讼代理人联系方式'] = lawfirm_resp2['通讯电话'] if '通讯电话' in lawfirm_resp2 else ""

    ret['诉讼请求'] = cause
    ret['起诉日期'] = dates
    ret['法院名称'] = court_name

    return http_api_call("get_company_sue_company", ret)


@register_tool
def company_sue_citizens_civil_complaint(plaintiff_name: Annotated[str, "原告人名称或者原告公司名称或者原告公司法人", True],
                                         defendant_name: Annotated[str, "被告人名称或者被告公司名称或者被告公司法人", True],
                                         plaintiff_lawfirm_name: Annotated[str, "原告律师事务所名称", True],
                                         defendant_lawfirm_name: Annotated[str, "被告律师事务所名称", True],
                                         dates: Annotated[str, "申诉日期", True],
                                         cause: Annotated[str, "上诉原因", True],
                                         court_name: Annotated[str, "上诉法院", True]) -> str:
    """
    通过原告公司，被告个人或者被告公司法人，原告辩护律师事务所，被告辩护律师事务所，诉讼时间，诉讼原因，受理法院等信息来生成一份民事诉讼状给受理法院
    例如：
    湖南中科电气股份有限公司与上海硅产业集团股份有限公司的法人发生了建设工程分包合同纠纷
    问题中出现 湖南中科电气股份有限公司 与 上海硅产业集团股份有限公司的法人 产生纠纷 则可以被判定为公司与个人产生纠纷
    """
    ret = {'原告': '-', '原告地址': '-', '原告法定代表人': '-', '原告联系方式': '-', '原告委托诉讼代理人': '-', '原告委托诉讼代理人联系方式': '-', '被告': '-',
           '被告性别': '-', '被告生日': '-', '被告民族': '-', '被告工作单位': '-', '被告地址': '-', '被告联系方式': '-', '被告委托诉讼代理人': '-',
           '被告委托诉讼代理人联系方式': '-', '诉讼请求': '-', '事实和理由': '上诉', '证据': 'PPPPP', '法院名称': '-', '起诉日期': '-'}

    # 获得原告个人的信息
    company_name = augment_company_name(plaintiff_name)[0]
    company_name2 = augment_company_name(defendant_name)[0]
    resp = http_api_call("get_company_info", {"query_conds": {"公司名称": company_name}, "need_fields": []})['return'][0]
    resp2 = http_api_call("get_company_info", {"query_conds": {"公司名称": company_name2}, "need_fields": []})['return'][0]

    lawfirm_resp = \
        http_api_call("get_lawfirm_info", {"query_conds": {"律师事务所名称": plaintiff_lawfirm_name}, "need_fields": []})[
            'return'][0]
    lawfirm_resp2 = \
        http_api_call("get_lawfirm_info", {"query_conds": {"律师事务所名称": defendant_lawfirm_name}, "need_fields": []})[
            'return'][0]

    if len(resp) > 0:
        ret['原告'] = company_name
        ret['原告地址'] = resp['办公地址'] if '办公地址' in resp else ""
        ret['原告法定代表人'] = resp['法人代表'] if "法人代表" in resp else ""
        ret['原告联系方式'] = resp['联系电话'] if '联系电话' in resp else ""
    if len(lawfirm_resp) > 0:
        ret['原告委托诉讼代理人'] = plaintiff_lawfirm_name
        ret['原告委托诉讼代理人联系方式'] = lawfirm_resp['通讯电话'] if '通讯电话' in lawfirm_resp else ""

    if len(resp2) > 0:
        ret['被告'] = resp2['法人代表'] if "法人代表" in resp2 else ""
        ret['被告工作单位'] = company_name2
        ret['被告地址'] = resp2['办公地址'] if '办公地址' in resp2 else ""
        ret['被告联系方式'] = resp2['联系电话'] if '联系电话' in resp2 else ""
    if len(lawfirm_resp2) > 0:
        ret['被告委托诉讼代理人'] = defendant_lawfirm_name
        ret['被告委托诉讼代理人联系方式'] = lawfirm_resp2['通讯电话'] if '通讯电话' in lawfirm_resp2 else ""

    ret['诉讼请求'] = cause
    ret['起诉日期'] = dates
    ret['法院名称'] = court_name

    return http_api_call("get_company_sue_citizens", ret)
