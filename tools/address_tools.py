import requests
from register.tool_register import register_tool, get_tools, dispatch_tool
from typing import get_origin, Annotated, Union, List, Optional
from schema.address_info import AddressInfo, AddressCode,AddressInfoEnum,AddressCodeEnum

api_list = [
    "get_address_info",
    "get_address_code",

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
def get_address_info(
        address:Annotated[str,"详细的地址信息",True],
)->AddressInfo:
    """
    地址类工具
    根据地址查该地址对应的省份城市区县
    """

    resp = http_api_call("get_address_info",{"query_conds":{"地址": address},"need_fields":[]})
    province = resp['return'][0]['省份']
    city = resp['return'][0]['城市']
    district = resp['return'][0]['区县']
    resp2 = http_api_call("get_address_code",{"query_conds":{"省份": province,"城市":city,"区县":district},"need_fields":[]})
    ret = resp['return'][0]
    ret2 = resp2['return'][0]
    ret.update(ret2)
    resp['return'][0] = ret
    return resp


@register_tool
def get_address_code(
        province:Annotated[str,"省份信息",True],
        city:Annotated[str,"城市信息",True],
        district:Annotated[str,"区县信息",True],

)->AddressCode:
    """
    地址类工具
    根据省市区查询区划代码
    """
    return http_api_call("get_address_code",{"query_conds":{"省份": province,"城市":city,"区县":district},"need_fields":[]})

