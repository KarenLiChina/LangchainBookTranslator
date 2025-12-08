from domain.page import Page


class Book:
    """
    需要翻译的书
    """

    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path
        self.pages = []  # 书的所有内容页

    def add_page(self, page: Page):
        self.pages.append(page)
