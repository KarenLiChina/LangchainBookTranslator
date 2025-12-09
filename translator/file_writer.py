import pandas as pd
from reportlab.lib import pagesizes, colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, PageBreak, Spacer

from domain.content import ContentType
from utils.log_utils import log


class FileWriter:

    def __init__(self, book):
        self.book = book

    def save_book(self, output_path: str = None, file_format: str = 'PDF'):
        """
        负责把翻译之后的数据写入到一个文件中
        :param output_path:
        :param file_format:
        :return:
        """
        print(file_format)
        if file_format.lower() == 'pdf':
            return self.save_book_pdf(output_path)
        elif file_format.lower() == 'markdown':
            return self.save_book_markdown(self.book)
        else:
            log.warning('当前项目文件格式不支持，项目仅支持 PDF，MarkDown')
            return ''

    def save_book_pdf(self, output_path: str = None):
        """
        把数据写入PDF文件中
        :param output_path:
        :return:
        """
        if not output_path:  # 默认情况，输出为原文件名_translated.pdf
            output_path = self.book.pdf_file_path.replace('.pdf', '_translated.pdf')

        # 写数据到文件中
        log.debug(f'pdf原文件路径是：{self.book.pdf_file_path}, 翻译之后的输出文件路径: {output_path}')

        # 1、先注册中文字体
        try:
            # 注册中文字体
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            log.info("成功注册 STSong-Light 字体")
        except Exception as e:
            log.error(f"注册字体失败: {e}")
            # 尝试注册其他字体
            try:
                pdfmetrics.registerFont(UnicodeCIDFont('STSongStd-Light'))
            except:
                log.warning("使用默认字体")

        # 2、创建一个pdf的文字段落样式
        try:
            style = ParagraphStyle('ChineseStyle', fontName='STSong-Light', fontSize=12, leading=14)
        except:
            style = ParagraphStyle('ChineseStyle', fontSize=12, leading=14)

        # 3、创建一个pdf的文档
        doc = SimpleDocTemplate(output_path, pagesize=pagesizes.letter)

        pdf_data = []  # 存放临时写入PDF文件的数据

        for page in self.book.pages:  # 循环这本书中所有的页
            for content in page.contents:
                if content.status:
                    # 分两种情况：文字段落和表格
                    if content.content_type == ContentType.TEXT:
                        # 写一个段落
                        try:
                            paragraph = Paragraph(text=content.translation, style=style)
                            pdf_data.append(paragraph)
                        except:
                            # 如果文本中有特殊字符，进行清理
                            cleaned_text = str(content.translation).replace('<', '&lt;').replace('>', '&gt;')
                            paragraph = Paragraph(text=cleaned_text, style=style)
                            pdf_data.append(paragraph)

                    elif content.content_type == ContentType.TABLE:
                        try:
                            print("=" * 50)
                            print(f"表格原始数据类型: {type(content.translation)}")

                            # 准备表格数据
                            table_data = []

                            # 检查数据格式并转换为合适的列表格式
                            if hasattr(content.translation, 'values'):
                                # 如果是 DataFrame
                                if not content.translation.empty:
                                    # 获取数据 - 添加列名作为第一行
                                    df_values = content.translation.values.tolist()
                                    if len(content.translation.columns) > 0:
                                        # 添加列标题
                                        table_data.append(content.translation.columns.tolist())
                                        table_data.extend(df_values)
                                    else:
                                        table_data = df_values
                                else:
                                    log.warning("DataFrame 为空")
                                    continue
                            elif isinstance(content.translation, list):
                                # 如果是列表
                                table_data = content.translation
                                print(f"表格数据为列表格式: {table_data}")
                            elif isinstance(content.translation, str):
                                # 如果是字符串，尝试解析
                                lines = content.translation.strip().split('\n')
                                for line in lines:
                                    # 清理和分割数据
                                    cells = [cell.strip() for cell in line.split(',') if cell.strip()]
                                    if cells:
                                        table_data.append(cells)
                            else:
                                log.error(f"未知的表格数据类型: {type(content.translation)}")
                                continue

                            print(f"表格数据行数: {len(table_data)}")
                            print(f"表格数据列数: {len(table_data[0]) if table_data else 0}")

                            if not table_data:
                                log.warning("表格数据为空，跳过")
                                continue

                            # 检查数据格式
                            if not all(isinstance(row, list) for row in table_data):
                                log.error("表格数据格式不正确")
                                continue

                            # 确定表格的列数（以第一行为准）
                            num_cols = len(table_data[0])

                            # 动态计算列宽
                            # 根据列数自动调整列宽，确保不超过页面宽度
                            page_width = pagesizes.letter[0]
                            available_width = page_width - doc.leftMargin - doc.rightMargin

                            # 计算每列的宽度（平均分配）
                            col_width = available_width / num_cols

                            # 创建表格样式
                            table_style = TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F81BD')),  # 蓝色表头
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'STSong-Light'),
                                ('FONTSIZE', (0, 0), (-1, 0), 12),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#D9E1F2')),  # 浅蓝色背景
                                ('FONTNAME', (0, 1), (-1, -1), 'STSong-Light'),
                                ('FONTSIZE', (0, 1), (-1, -1), 10),
                                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ])

                            # 创建表格对象 - 关键修改：不使用固定的 inch 单位，而是使用计算出的列宽
                            table = Table(
                                data=table_data,
                                colWidths=[col_width] * num_cols,
                                rowHeights=None  # 让系统自动计算行高
                            )

                            # 为长文本单元格添加自动换行样式
                            table_style.add('WORDWRAP', (0, 0), (-1, -1), True)

                            table.setStyle(table_style)
                            pdf_data.append(table)

                            # 在表格后面添加一些空白
                            pdf_data.append(Spacer(1, 12))

                        except Exception as e:
                            log.error(f"处理表格时出错: {e}")
                            import traceback
                            traceback.print_exc()
                            # 如果表格创建失败，尝试以文本形式显示
                            error_msg = f"[表格数据，处理出错: {str(e)[:50]}...]"
                            paragraph = Paragraph(text=error_msg, style=style)
                            pdf_data.append(paragraph)

            # 当前这一页的内容都处理了，紧跟着接一条分页符
            # 分页符不能加在最后一页
            if page != self.book.pages[-1]:
                pdf_data.append(PageBreak())  # 除了最后一页，每页的后面都加上一个分页符

        try:
            doc.build(pdf_data)
            log.info('pdf文件写入完成！')
            return output_path
        except Exception as e:
            log.error(f"PDF构建失败: {e}")
            import traceback
            traceback.print_exc()
            raise

    def save_book_markdown(self, output_path: str = None):
        """
        把数据写入MarkDown文件中
        :param output_path:
        :return:
        """
        if not output_path:  # 默认情况，输出为原文件名_translated.md
            output_path = self.book.pdf_file_path.replace('.pdf', '_translated.md')
            # 写数据到文件中
            log.debug(f'原文件路径是：{self.book.file_path}, 翻译之后的输出文件路径: {output_path}')

            with open(output_path, 'w', encoding='UTF-8') as md_file:
                for page in self.book.pages:  # 循环这本书中所有的页
                    for content in page.contents:
                        if content.status:
                            # 分两种情况：文字段落和表格
                            if content.content_type == ContentType.TEXT:
                                # 写一个段落
                                md_file.write(content.translation + '\n\n')

                            elif content.content_type == ContentType.TABLE:
                                # 写入一个表格
                                df: pd.DataFrame = content.translation  # 翻译之后的表格数据
                                first_row = df.values.tolist()[0]
                                df.columns = first_row
                                df.drop([0], inplace=True)
                                header = '| ' + ' | '.join(
                                    [str(column_name) for column_name in df.columns]) + ' |' + '\n'
                                tr = '| ' + ' | '.join(['---'] * len(df.columns)) + ' |' + '\n'
                                t_body = '\n'.join(['| ' + ' | '.join(str(cell) for cell in row) + ' |' for row in
                                                    df.values.tolist()]) + '\n\n'
                                md_file.write(header + tr + t_body)

                    # 当前这一页的内容都处理了， 紧跟着接一条分页符
                    # 分页符不能加在最后一页
                    if page != self.book.pages[-1]:
                        md_file.write('\n -----\n\n')  # 除了最后一页，每页的后面都加上一个分页符

            log.info('MarkDown文件写入完成！')
            return output_path
