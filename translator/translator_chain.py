from ai_model.model import Model
from domain.content import Content


class TranslatorChain:
    """
    负责调用LangChain来完成文本的翻译，chain对象，可以是单例的，不需要每次都初始化。
    """

    _instance = None

    def __init__(self, model: Model):
        self.langchain = model.make_prompt() | model.create_llm()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TranslatorChain, cls).__new__(cls)  # 调用父类的构造函数，创建ProjectConfig
        return cls._instance

    def run(self, content: Content, source_language: str, target_language: str):
        """
        翻译具体的文本，返回翻译之后的文本内容和翻译成功的状态
        :param content:
        :param source_language:
        :param target_language:
        :return: translate_text, status
        """
        pass
