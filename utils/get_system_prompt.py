from classify_query import route
from schema.address_info import address_schema
from schema.weather_info import weather_schema
from schema.consumption_restriction_info import consumptionrestriction_schema
from schema.legal_info import legal_schema
from schema.company_info import company_schema
from schema.court_info import court_schema
from schema.lawfirm_info import lawfirm_schema



def get_system_prompt(query):
    info = route(query)

    system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
    """

    if '公司' not in info and '案件' not in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" in info and  "限制高消费" not in info and "天气" not in info  and "地址" not in info:
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """
        from tools.lawsuit_document_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool
    #公司类问题
    if '公司' in info and '案件' not in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" not in info  and "地址" not in info:
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + company_schema
        from tools.company_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #案件类问题
    if '公司' not in info and '案件' in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" not in info  and "地址" not in info:
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + legal_schema
        from tools.legal_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #法院类问题
    if '公司' not in info and '案件' not in info and "法院" in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" not in info  and "地址" not in info:
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + court_schema
        from tools.court_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #律师事务所类问题
    if '公司' not in info and '案件' not in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" not in info  and "地址" not in info:
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + lawfirm_schema
        from tools.lawfirm_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool


    #限制消费类问题
    if '公司' not in info and '案件' not in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" in info and "天气" not in info  and "地址" not in info:
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + consumptionrestriction_schema
        from tools.consumption_restriction_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #天气类问题
    if '公司' not in info and '案件' not in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" in info  and "地址" not in info:
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + weather_schema
        from tools.weather_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #地址类问题
    if '公司' not in info and '案件' not in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" not in info  and "地址" in info:
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + address_schema
        from tools.address_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #公司、地址类问题
    if '公司' in info and '案件' not in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" not in info  and "地址" in info:
        data_schema = company_schema+address_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.address_tools import get_tools,dispatch_tool
        from tools.company_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #公司、地址、天气类问题
    if '公司' in info and '案件' not in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" in info and "地址" in info:
        data_schema = company_schema+address_schema+weather_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.address_tools import get_tools,dispatch_tool
        from tools.company_tools import get_tools,dispatch_tool
        from tools.weather_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #法院、地址类问题
    if '公司' not in info and '案件' not in info and "法院" in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" not in info  and "地址" in info:
        data_schema = court_schema+address_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.address_tools import get_tools,dispatch_tool
        from tools.court_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    #法院、地址、天气类问题
    if '公司' not in info and '案件' not in info and "法院" in info and "律师事务所" not in info and "书写诉讼状" not in info and  "限制高消费" not in info and "天气" in info and "地址" in info:
        data_schema = court_schema+address_schema+weather_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.address_tools import get_tools,dispatch_tool
        from tools.court_tools import get_tools,dispatch_tool
        from tools.weather_tools import get_tools,dispatch_tool
        return system_prompt,get_tools,dispatch_tool

    # 律师事务所、地址类问题
    if '公司' not in info and '案件' not in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" in info:
        data_schema = lawfirm_schema + address_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.address_tools import get_tools, dispatch_tool
        from tools.lawfirm_tools import get_tools, dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 律师事务所、地址、天气类问题
    if '公司' not in info and '案件' not in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" in info and "地址" in info:
        data_schema = lawfirm_schema + address_schema+weather_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.address_tools import get_tools, dispatch_tool
        from tools.lawfirm_tools import get_tools, dispatch_tool
        from tools.weather_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool


    # 公司，案件类问题
    if '公司' in info and '案件' in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" not in info:
        data_schema = company_schema+legal_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools, dispatch_tool
        from tools.legal_tools import get_tools, dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 法院，案件类问题
    if '公司' not in info and '案件' in info and "法院" in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" not in info:
        data_schema = court_schema+legal_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.court_tools import get_tools, dispatch_tool
        from tools.legal_tools import get_tools, dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 法院，案件类问题
    if '公司' in info and '案件' in info and "法院" in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" not in info:
        data_schema = court_schema+legal_schema+company_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.court_tools import get_tools, dispatch_tool
        from tools.legal_tools import get_tools, dispatch_tool
        from tools.company_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 律师事务所，案件类问题
    if '公司' not in info and '案件' in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" not in info:
        data_schema = lawfirm_schema+legal_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.lawfirm_tools import get_tools, dispatch_tool
        from tools.legal_tools import get_tools, dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 律师事务所，案件类问题
    if '公司' in info and '案件' in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" not in info:
        data_schema = lawfirm_schema+legal_schema+company_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.lawfirm_tools import get_tools, dispatch_tool
        from tools.legal_tools import get_tools, dispatch_tool
        from tools.company_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 律师事务所，法院，案件类问题
    if '公司' in info and '案件' in info and "法院" in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" not in info:
        data_schema = lawfirm_schema+legal_schema+company_schema+court_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.lawfirm_tools import get_tools, dispatch_tool
        from tools.legal_tools import get_tools, dispatch_tool
        from tools.company_tools import get_tools,dispatch_tool
        from tools.court_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 律师事务所，法院，限制高消费，案件类问题
    if '公司' in info and '案件' in info and "法院" in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" not in info:
        data_schema = lawfirm_schema+legal_schema+company_schema+court_schema+consumptionrestriction_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.lawfirm_tools import get_tools, dispatch_tool
        from tools.legal_tools import get_tools, dispatch_tool
        from tools.company_tools import get_tools,dispatch_tool
        from tools.court_tools import get_tools,dispatch_tool
        from tools.consumption_restriction_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 限制高消费类问题
    if '公司' in info and '案件' not in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" in info and "天气" not in info and "地址" not in info:
        data_schema = company_schema+consumptionrestriction_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.consumption_restriction_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 限制高消费 案件类问题
    if '公司' in info and '案件' in info and "法院" not in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" in info and "天气" not in info and "地址" not in info:
        data_schema = company_schema+consumptionrestriction_schema+legal_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.consumption_restriction_tools import get_tools,dispatch_tool
        from tools.legal_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 限制高消费 法院类问题
    if '公司' in info and '案件' not in info and "法院"  in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" in info and "天气" not in info and "地址" not in info:
        data_schema = company_schema+consumptionrestriction_schema+court_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.consumption_restriction_tools import get_tools,dispatch_tool
        from tools.court_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 限制高消费 法院类问题
    if '公司' in info and '案件' in info and "法院"  in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" in info and "天气" not in info and "地址" not in info:
        data_schema = company_schema+consumptionrestriction_schema+court_schema+legal_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.consumption_restriction_tools import get_tools,dispatch_tool
        from tools.court_tools import get_tools,dispatch_tool
        from tools.legal_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 限制高消费 律所类问题
    if '公司' in info and '案件' not in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" in info and "天气" not in info and "地址" not in info:
        data_schema = company_schema+consumptionrestriction_schema+lawfirm_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.consumption_restriction_tools import get_tools,dispatch_tool
        from tools.lawfirm_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 限制高消费 律所 案件类问题
    if '公司' in info and '案件' in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" in info and "天气" not in info and "地址" not in info:
        data_schema = company_schema+consumptionrestriction_schema+lawfirm_schema+legal_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.consumption_restriction_tools import get_tools,dispatch_tool
        from tools.lawfirm_tools import get_tools,dispatch_tool
        from tools.legal_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 律所 案件 地址类问题
    if '公司' in info and '案件' in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气" not in info and "地址" in info:
        data_schema = company_schema+lawfirm_schema+legal_schema+address_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.lawfirm_tools import get_tools,dispatch_tool
        from tools.legal_tools import get_tools,dispatch_tool
        from tools.address_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 律所 案件 地址 天气类问题
    if '公司' in info and '案件' in info and "法院" not in info and "律师事务所" in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气"  in info and "地址" in info:
        data_schema = company_schema+lawfirm_schema+legal_schema+address_schema+weather_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.lawfirm_tools import get_tools,dispatch_tool
        from tools.legal_tools import get_tools,dispatch_tool
        from tools.address_tools import get_tools,dispatch_tool
        from tools.weather_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 案件 地址 天气 法院类问题
    if '公司' in info and '案件' in info and "法院" in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气"  in info and "地址" in info:
        data_schema = company_schema+legal_schema+address_schema+weather_schema+court_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.legal_tools import get_tools,dispatch_tool
        from tools.address_tools import get_tools,dispatch_tool
        from tools.weather_tools import get_tools,dispatch_tool
        from tools.court_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool

    # 公司 案件 地址 法院类问题
    if '公司' in info and '案件' in info and "法院" in info and "律师事务所" not in info and "书写诉讼状" not in info and "限制高消费" not in info and "天气"  not in info and "地址" in info:
        data_schema = company_schema+legal_schema+address_schema+court_schema
        system_prompt = """你是一位金融法律专家，你的任务是根据用户给出的query，调用给出的工具接口，获得用户想要查询的答案。
        所提供的工具接口可以查询数据表的信息，数据表的schema如下:
        """ + data_schema
        from tools.company_tools import get_tools,dispatch_tool
        from tools.legal_tools import get_tools,dispatch_tool
        from tools.address_tools import get_tools,dispatch_tool
        from tools.court_tools import get_tools,dispatch_tool
        return system_prompt, get_tools, dispatch_tool



    return system_prompt


















