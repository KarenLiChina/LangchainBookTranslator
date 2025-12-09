import gradio as gr

from ai_model.openai_model import OpenAIModel
from translator.book_translator import PDFTranslator
from utils.project_config import ProjectConfig


def init_translator():
    config = ProjectConfig()
    config.initialize()

    # 初始化大语言模型
    if config.model_type == 'OpenAIModel':
        model = OpenAIModel(config.model_name, config.api_key, config.base_url)
    else:
        # model = ChatGLMModel(config.model_name, config.api_key, config.base_url)
        pass
    # 初始化一个翻译器
    global translator
    translator = PDFTranslator(model)


def translate(input_file, source_language, target_language):
    output_file = translator.translate_book(file_path=input_file, source_language=source_language,
                                            target_language=target_language,out_file_format='pdf')
    return output_file


def run_gradio():
    """
    启动Gradio
    :return:
    """
    instance = gr.Interface(
        fn=translate,  # 调用翻译书籍的函数
        title='自动翻译器',
        inputs=[
            gr.File(label='上传PDF书籍文件'),  # 需要用户上传文件
            gr.Textbox(label='源语言(默认是：英文)', placeholder='English', value='English'),
            gr.Textbox(label='目标语言(默认是：中文)', placeholder='中文', value='中文')
        ],
        outputs=[
            gr.File(label='下载翻译之后的文件')
        ]
    )
    instance.launch(server_name='0.0.0.0', server_port=8008, share=True)


if __name__ == '__main__':
    init_translator()
    run_gradio()
