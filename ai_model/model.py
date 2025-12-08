from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate


class Model:
    """
    AI的模型对象，抽象类OL
    """

    def create_llm(self):
        print("create llm")

    def make_prompt(self):
        """
        创建发送给大语言模型的提示模板
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template("""
        你是一个翻译专家，精通各种人类的语言。
        输入的是：{source_language} 语言，翻译之后的语言为{target_language}""")
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")  # 用户真正翻译的提示是动态的，直接将用户的要求传进来
        return ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
