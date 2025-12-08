from enum import Enum, auto

import pandas as pd
from utils.log_utils import log


class ContentType(Enum):
    """
    内容的类型，枚举
    """
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()


class Content:
    """书中的内容"""

    def __init__(self, content_type: ContentType, original, translation=None):
        """
        内容初始化
        :param type: 类型
        :param original: 原文
        :param translation: 翻译
        """
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False  # 翻译完成的状态

    def set_translation(self, translation, status):
        """
        设置翻译之后的文本，和翻译的状态
        :param translation:
        :param status:
        :return:
        """
        if self.content_type == ContentType.TEXT and isinstance(translation, str) and status == True:
            self.translation = translation
            self.status = status
        else:
            log.warning('当前输出的翻译不是文本类型')

    def check_translation_type(self, translation):
        pass

    def get_original_to_string(self):
        return self.original


class TableContent:
    """表格中的内容"""

    def __init__(self, content_type: ContentType, original, translation=None):
        """
        内容初始化
        :param type: 类型
        :param original: 表格原始内容
        :param translation: 翻译
        """
        df = pd.DataFrame(original)
        self.content_type = content_type
        self.original = df
        self.translation = translation
        self.status = False  # 翻译完成的状态

    @log.catch
    def set_translation(self, translation, status):
        """
        设置翻译之后的文本，和翻译的状态
        1. 判断数据的合法性
        2. 把translation文本数据 变成二维数组（表格）
        3. 把二维数组变成DataFrame
        :param translation:
        :param status:
        :return:
        """
        if self.content_type == ContentType.TABLE and isinstance(translation, str) and status == True:
            # 得到二维数组
            table_data = [row.strip().split() for row in translation.strip().split('\n')]
            log.debug(table_data)
            # 得到dataframe数据，表头单独处理
            translation_df = pd.DataFrame(table_data[1:], columns=table_data[0])
            log.debug(f'处理成DataFrame数据：\n{translation_df}')
            self.translation = translation_df
            self.status = status

    def check_translation_type(self, translation):
        pass

    def get_original_to_string(self):
        """ 把dataframe对象变成字符串"""
        return self.original.to_string(header=False, index=False)
