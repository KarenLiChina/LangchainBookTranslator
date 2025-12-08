from typing import Optional

from ai_model.model import Model
from utils.log_utils import log
from .file_writer import FileWriter
from .pdf_parser import parse_pdf
from .translator_chain import TranslatorChain


class PDFTranslator:
    """
    翻译PDF文件的书籍
    """

    def __init__(self, model: Model):
        self.book = None
        self.chain = TranslatorChain(model)  # 真正负责翻译文本内容
        self.writer = FileWriter(self.book)

    def translate_book(self, file_path: str, out_file_format: str, source_language: str,
                       target_language: str,
                       out_file_path: str = None, pages: Optional[int] = None):
        """
        翻译一本书
        :param file_path: 文件路径
        :param out_file_format: 输出文件格式
        :param source_language: 书籍中的原始语言
        :param target_language: 翻译之后的目标语言
        :param out_file_path: 翻译后的文件存放路径
        :param pages: 需要翻译的页码，如果不传，则翻译整本书
        :return:
        """
        self.book = parse_pdf(file_path, pages)  # 解析文件得到一个book对象
        self.writer.book = self.book
        for page_index, page in enumerate(self.book.pages):
            for content_index, content in enumerate(page.contents):
                # 使用Langchain翻译每一页的内容
                translation_text, status = self.chain.run(content, source_language, target_language)

                log.debug(f'翻译之后的内容是：{translation_text}')
                # 把翻译之后的文本和状态设置到content对象中
                self.book.pages[page_index].contents[content_index].set_translation(translation_text, status)

        # 把翻译后的数据写入文件 Writer
        self.writer.save_book(out_file_path, out_file_format)
