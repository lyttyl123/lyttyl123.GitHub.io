import pandas as pd
import matplotlib.pyplot as plt
import gradio as gr
import seaborn as sns
from gradio import update
from langchain_openai import ChatOpenAI
# 创建数据分析代理
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_experimental.tools import PythonAstREPLTool
import os
import io
import contextlib
import sys
import re
from dotenv import load_dotenv

load_dotenv('deepseek-key.env')
# 设置matplotlib  中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'SimHei', 'Microsoft YeHei']
plt.rcParams['axes.unicode_minus'] = False


class CodeCapture:
    def __init__(self):
        # 初始化捕获代码列表
        self.code = []
        # 初始化捕获输出列表
        self.output = []

    # 清理特殊字符和颜色
    def clean_ansi_codes(self, text):
        # 使用正则表达式匹配ANSI颜色代码
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        # 替代ANSI颜色代码为空字符串
        return ansi_escape.sub('', text)

    def clean_conde(self, code):
        # 先清理ANSI颜色代码
        code = self.clean_ansi_codes(code)
        # 去除首位的空白字符
        code = code.strip()
        # 检测代码是否以代码块标记开头
        if code.startswith("```python"):
            # 去除代码块标记
            code = code[9:].strip()
        # 检测代码是否以代码块标记开头
        if code.startswith("```"):
            # 去除代码块标记
            code = code[3:].strip()
        # 检测代码是否以代码块标记结尾
        if code.endswith("```"):
            # 去除代码块标记
            code = code[:-3].strip()
        # 返回清理后的代码
        return code

    def write(self, text):
        # 将捕获的输出内容添加到self.output列表
        self.output.append(text)
        # 检查输出内容中是否包含特定的字符标记（Action和Action Input）
        if "Action:" in text and "Action Input:" in text:
            # 使用正则表达式匹配代码片段
            code_match = re.search(r"Action Input:(.*?)(?=\nObservation:|$)", text, re.DOTALL)
            if code_match:
                # 提取匹配到的代码片段
                code = code_match.group(1).strip()
                # 清理代码片段
                code = self.clean_conde(code)
                # 如果清理后的代码片段非空，添加到self.code列表
                if code:
                    self.code.append(code)

    def get_code(self):
        return '\n'.join(self.code)

    def get_output(self):
        return ''.join(self.output)


'''
创建一个数据分析应用类，用于处理数据文件和执行数据分析
'''


class DataAnalysisApp:
    def __init__(self):
        # 初始化数据框为空
        self.df = None
        # 初始化数据分析代理为空
        self.agent = None
        # 初始化捕获代码器为空
        self.code_capture = None

    def create_agent(self):
        if self.df is not None:
            self.agent = create_pandas_dataframe_agent(
                ChatOpenAI(
                    temperature=0,
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个专业的数据分析师，请用中文回答所有问题。"}
                    ]
                ),
                self.df,
                verbose=True,  # 代理在运行时会输出详细信息，方便调试和监控
                agent_type="zero-shot-react-description",  # 快速响应
                allow_dangerous_code=True
            )

    # 处理上传文件
    def process_file(self, file):
        if file is None:
            return "请上传文件", None
        # 获取文件的扩展名
        file_ext = os.path.splitext(file.name)[1].lower()
        try:
            if file_ext == '.csv':
                self.df = pd.read_csv(file.name)
            elif file_ext == ['.xlsx', '.xls']:
                self.df = pd.read_excel(file.name)
            else:
                return "不支持的文件类型，请上传excel文件", None
            self.create_agent()

            return f"文件加载成功，数据形状，{self.df.shape}", self.df.head().to_html()
        except Exception as e:
            return f"处理文件时出错：{str(e)}", None

    def analyze_data(self, question):
        # 分析数据代码
        if self.df is None:
            return "请先上传数据文件", None

        if self.agent is None:
            return "Agent没有初始化", None

        try:
            self.code_capture = CodeCapture()
            # 捕获标准输出，将输出重定向到代码捕获的一个实例
            with contextlib.redirect_stdout(self.code_capture):
                result = self.agent.invoke({"input": question})

            # 从代码捕获的实例中获取执行的代码
            enecuated_code = self.code_capture.get_code()
            # 将提示信息打印到终端
            sys.__stdout__.write(f"Captured Output:{self.code_capture.get_code()}\n")
            sys.__stdout__.write(f"Enecuated_code:{enecuated_code}\n")
            sys.__stdout__.write(f"Result:{result}\n")

            # 检查是否生成图表
            if plt.get_fignums():
                plt.savefig('tem_plot.png')
                # 关闭图标，避免内存泄露
                plt.close()
                return result["output"], "tem_plot.png", enecuated_code

            return result["output"], None, enecuated_code

        except Exception as e:
            sys.__stdout__.write(f"Error:{str(e)}\n")
            return f"分析过程出错：{str(e)}", None, ""


# 创建应用实例
app = DataAnalysisApp()
with gr.Blocks() as ok:
    gr.Markdown("# 智能分析助手")
    with gr.Row():
        with gr.Column(1):
            file_input = gr.File(label="上传数据文件（CSV或Excel）")

            upload_output = gr.Textbox(label="上传状态")
        with gr.Column(2):
            data_preview = gr.HTML(label="数据预览")

            file_input.upload(
                app.process_file,
                inputs=[file_input],
                outputs=[upload_output, data_preview]
            )

    with gr.Row():
        question_input = gr.Textbox(
            label="输入您分析的问题",
            placeholder="例如：计算每列的基本统计信息"
        )

    with gr.Row():
        with gr.Column():
            analysis_output = gr.Textbox(
                label="分析结果",
            )
            code_output = gr.Code(
                label="执行的代码",
                language="python",
                interactive=False  # 表示代码不可执行
            )
        with gr.Column():
            plot_image = gr.Image(
                label="可视化结果"
            )
    question_input.submit(
        app.analyze_data,
        inputs=[question_input],
        outputs=[analysis_output, plot_image , code_output]
    )

if __name__ == '__main__':
    ok.launch()
