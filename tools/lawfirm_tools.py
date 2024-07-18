import requests
from tool_register.tool_register import register_tool, get_tools, dispatch_tool
from typing import get_origin, Annotated, Union, List, Optional
from schema.lawfirm_info import LawfirmInfo, LawfirmLog,LawfirmInfoEnum,LawfirmLogEnum

api_list = [
    "get_lawfirm_info",
    "get_lawfirm_log",

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
def get_lawfirm_info(
        lawfirm_name:Annotated[str,"律师事务所名称",True],
)->LawfirmInfo:
    """通过律师事务所名称获取律师事务所的信息"""
    resp = http_api_call("get_lawfirm_info",{"query_conds": {"律师事务所名称": lawfirm_name}, "need_fields": []})
    resp2 = http_api_call("get_lawfirm_log",{"query_conds": {"律师事务所名称": lawfirm_name}, "need_fields": []})

    resp['return'][0].update(resp2['return'][0])

    return resp