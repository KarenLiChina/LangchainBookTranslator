import gradio as gr


def calculate(num1, operation: str, num2):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 != 0:
            return num1 / num2
        else:
            raise gr.Error('除数不能为0。')
    return None


instance = gr.Interface(  # 构建UI 界面
    fn=calculate,  # 函数的输入要和inputs的个数保持一致，输出和output 保持一致
    inputs=[
        'number',  # number 对应数字组件， 等同于gr.Number
        gr.Radio(choices=['+', '-', '*', '/'], label='计算法则', value='+'),  # 单选项, value是默认值
        'number'
    ],
    outputs='number'

)

instance.launch(server_name='0.0.0.0',server_port=8008,auth=('admin','admin'))  # 启动 需要share 为true,server_name 默认为 127.0.0.1, 外网无法看到，写成0.0.0.0后，需要通过自己的ip地址访问