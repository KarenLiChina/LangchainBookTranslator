import time

import gradio as gr


def process_text(text: str, progress=gr.Progress()):  # 定义回调函数，并初始化一个进度条
    res = ''
    progress(0, desc='开始....')
    # 进度条滚动
    for letter in progress.tqdm(text,'运行中...'): # tqdm对 text 进行切割
        time.sleep(0.25)
        res += letter
    return res


instance = gr.Interface(  # 构建UI 界面
    fn=process_text,  # 函数的输入要和inputs的个数保持一致，输出和output 保持一致
    inputs=[
        gr.Text(label='请输入任何文本')
    ],
    outputs=gr.Text(label='输出结果')

)

instance.launch(server_name='0.0.0.0', server_port=8008,share=True)  # 启动 需要share 为true,server_name 默认为 127.0.0.1, 外网无法看到，写成0.0.0.0后，需要通过自己的ip地址访问
