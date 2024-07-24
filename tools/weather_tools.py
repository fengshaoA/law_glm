import requests
from register.tool_register import register_tool, get_tools, dispatch_tool
from typing import get_origin, Annotated, Union, List, Optional
from schema.weather_info import WeatherInfo,WeatherInfoEnum


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
def get_weather_info(
        province:Annotated[str,"省份名称",True],
        city:Annotated[str,"城市信息",True],
        dates:Annotated[str,"日期",True],
)->WeatherInfo:
    """
    天气类工具
    根据日期，省份，城市信息查询天气相关信息,这里需要注意：dates类型应该是2020年1月4日,不需要转化成2020-01-04这种格式
    """
    return http_api_call("get_temp_info",{"query_conds":{"省份": province, "城市": city, "日期":dates},"need_fields":[]})
