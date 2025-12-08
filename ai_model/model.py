class Model:
    """
    AI的模型对象，抽象类OL
    """

    def create_llm(self):
        print("create llm")
    # def make_prompt(self, content, target_language):
    #     """
    #     创建发送给大语言模型的提示文本
    #     :param content:
    #     :param target_language:
    #     :return:
    #     """
    #     if content.content_type == ContentType.TEXT:
    #         return f'请翻译成{target_language}：{content.original}'
    #
    #     if content.content_type == ContentType.TABLE:
    #         return f'请翻译成{target_language}，并且保持间距（可以用空格或者分隔符），并且以表格的形式返回：\n {content.get_original_to_string()}'
