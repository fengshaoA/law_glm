import requests
from tool_register.tool_register import register_tool, get_tools, dispatch_tool
from typing import get_origin, Annotated, Union, List, Optional
from schema.court_info import CourtInfo, CourtCode,CourtInfoEnum,CourtCodeEnum

api_list = [
    "get_court_info",
    "get_court_code",

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

@register_tool
def get_court_info(
        court_name:Annotated[str,"法院名称",True],
)->CourtInfo:
    """
    法院类工具
    根据法院名称查询法院名录相关信息
    """
    resp = http_api_call("get_court_info",{"query_conds": {"法院名称": court_name},"need_fields":[]})
    court_name = resp['return'][0]['法院名称']
    resp2 = http_api_call("get_court_code",{"query_conds": {"法院名称": court_name},"need_fields":[]})
    resp['return'][0].update(resp2['return'][0])
    return resp



@register_tool
def get_court_code(
        court_info:Annotated[str,'法院名称或者法院代字',True],
)->CourtCode:
    """
    法院类工具
    根据法院名称或者法院代字查询法院代字等相关数据;
        如果是是法院名称的时候，你直接从问题中提取法院名称；
        如果传入的是法院代字，你可以直接从问题中提取法院代字
        如果是传入值是案号：案号可分为以下几种：
            1.如果 court_info = (2019)苏民申6268号 其中(2019)是起诉日期，苏是法院代字，民申6268号是案件类型号；则返回court_info =苏 进入工具调用.
            2.如果 court_info =(2019)沪0115民初61975号 其中(2019)是起诉日期，沪0115是法院代字，民初61975号是案件类型号；则返回court_info=沪0115 进入工具调用.
            3.如果 court_info =【2021】豫0304民初300号 其中【2021】是起诉日期，豫0304 是法院代字，民初300号是案件类型号；则返回court_info=豫0304 进入工具调用.
            4.如果 court_info =(2021)粤粤03民终12893号 你可以识别出 这个案号是一个出现重复字的案号，重复的字是粤，更新后的案号应该是(2021)粤03民终12893号，根据上面的案例，则返回court_info=粤03 进入工具调用.
            5.如果 court_info =（2019）鲁0112民初8973号.txt 或者 （2019）鲁0112民初8973号 和上面类似，则返回court_info= 鲁0112 进入工具调用.


    """

    resp = http_api_call("get_court_code",{"query_conds": {"法院名称": court_info},"need_fields":[]})
    if int(resp['return_items_count']) >0:
        court_name = resp['return'][0]['法院名称']
        resp2 = http_api_call("get_court_info", {"query_conds": {"法院名称": court_name}, "need_fields": []})
        resp['return'][0].update(resp2['return'][0])
        return resp

    if len(court_info)>8:
        case_num = court_info.replace('（', '(').replace('）', ')').replace('【', '(').replace('】', ')').replace('[',
                                                                                                             '(').replace(
            ']', ')')
        if ')' in str(case_num):
            court_code_temp = str(case_num).strip().split(')')[1]
        else:
            court_code_temp = str(case_num)[4:]

        court_info = str()
        for idx in range(len(court_code_temp)):
            if idx == 0:
                court_info += court_code_temp[idx]
            else:
                if str(court_code_temp[idx]).isdigit():
                    court_info += court_code_temp[idx]
                else:
                    break

    resp =  http_api_call("get_court_code", {"query_conds": {"法院代字": court_info}, "need_fields": []})
    court_name = resp['return'][0]['法院名称']
    resp2 = http_api_call("get_court_info", {"query_conds": {"法院名称": court_name}, "need_fields": []})
    resp['return'][0].update(resp2['return'][0])
    return resp
