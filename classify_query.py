from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from langchain_openai import ChatOpenAI

glm = ChatOpenAI(
    temperature=0.95,
    model="glm-4",
    openai_api_key="",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)


template = """Assess the user’s question to determine if it belongs to the following categories: company, legal, court-related, lawfirm-related, lawsuit document-related, high-end consumption restriction-related, weather or temperature-related, or address-related.
Please list all the categories you think are relevant.
Do not respond with more than one word.
<question>
{question}
</question>

Classification:
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


print(route("北京丰台区人民法院的代字和行政级别是？"))