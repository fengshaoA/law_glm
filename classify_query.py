from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from langchain_openai import ChatOpenAI

glm = ChatOpenAI(
    temperature=0.1,
    model="glm-4",
    openai_api_key="",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)


template = """
你是一位问题分类的专家，能够对用户的query进行精准的分类，并且的用户的问题有可能不是一个单独类别，有可能是多个类。
目前用户的问题只包含在如下类别中：
    1. 公司类
    2. 案件类
    3. 律师事务所类
    4. 法院类
    5. 书写诉讼状类
        如果被分类为书写诉讼状类的问题，需要给出是一下那类纠纷，并且只可能是下面的一类。
            - 公司与公司产生纠纷
            - 公司与公司法人（个人）产生纠纷
            - 公司法人（个人）与公司产生纠纷
            - 公司法人（个人）与公司法人（个人）产生纠纷
    6. 限制高消费类
    7. 天气温度类
    8. 地址类
请准确的对用户的query进行分类，分类结果必须实事求是，不要自己发挥。
分类结果中不要包含与用户query无关的类别。
你回答结果尽量精简，不要给出与分类无关的信息。


<问题>
{question}
</问题>

分类：
"""

router_chain = (
        PromptTemplate.from_template(template)
        | glm
        | StrOutputParser()
)

def route(query, debug=False):
    info = router_chain.invoke({
        "question": query
    })

    return str(info)

# print(route("赛轮集团股份有限公司与晶瑞电子材料股份有限公司发生了买卖合同纠纷，赛轮集团股份有限公司委托给了安徽安康律师事务所，晶瑞电子材料股份有限公司委托给了安徽奥成律师事务所，请写一份民事起诉状给公安县人民法院时间是2024-01-01"))