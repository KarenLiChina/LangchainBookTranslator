class PageOutOfRangeException(Exception):

    def __init__(self, book_total, request_number):
        self.book_total = book_total
        self.request_number = request_number
        super().__init__(f'页码的范围越界：这本书的总页数为：{self.book_total}，要求输出的页数为{self.request_number}')
