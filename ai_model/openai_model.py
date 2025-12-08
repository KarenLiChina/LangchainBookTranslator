from langchain_openai import ChatOpenAI

from ai_model.model import Model


class OpenAIModel(Model):

    def __init__(self, model_name, api_key, base_url):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url

    def create_llm(self):
        """
        初始化 openai 大语言模型对象
        :return:
        """
        return ChatOpenAI(model=self.model_name,
                          api_key=self.api_key,
                          base_url=self.base_url,
                          temperature=0)
