import time

import gradio as gr


def process_text(text: str):  # 定义回调函数，并初始化一个进度条
    resp = None
    for char in text:
        resp += char
        time.sleep(1)
        yield resp


instance = gr.Interface(  # 构建UI 界面
    fn=process_text,  # 函数的输入要和inputs的个数保持一致，输出和output 保持一致
    inputs=[
        gr.Text(label='请输一个提问')
    ],
    outputs=gr.Text(label='输出结果'),
    title="模拟流式输出"

)

def chat(message, history):  # 定义回调函数，并初始化一个进度条
    resp = ''
    response='很高兴和你聊天！'
    for char in response:
        resp += char
        time.sleep(1)
        yield resp

instance_chat = gr.ChatInterface(  # 构建UI 界面
     fn=chat,  # 函数的输入要和inputs的个数保持一致，输出和output 保持一致
    # inputs=[
    #     gr.Text(label='请输一个提问')
    # ],
    # outputs=gr.Text(label='输出结果'),
     title="模拟流式输出"

)

instance_chat.launch(server_name='0.0.0.0', server_port=8008,
                share=True)  # 启动 需要share 为true,server_name 默认为 127.0.0.1, 外网无法看到，写成0.0.0.0后，需要通过自己的ip地址访问
