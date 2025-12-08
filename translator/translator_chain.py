from ai_model.model import Model
from domain.content import Content, ContentType
from utils.log_utils import log


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
        text = ''
        result = ''
        try:
            # 提示模板中的三个变量
            if content.content_type == ContentType.TEXT:
                text = f"请按照要求翻译一下的内容:{content.original}"
            elif content.content_type == ContentType.TABLE:
                text = f"请按照要求翻译一下的内容，以非Markdown的表格形式返回:\n {content.get_original_to_string()}"

            result = self.langchain.invoke({
                'source_language': source_language,
                'target_language': target_language,
                'text': text
            })
            log.info(result.content)
        except Exception as e:
            log.exception(e)
            return result, False  # 报错时候返回False
        return result.content, True
