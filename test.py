# test.py 文件
import base64
import os
from idlelib import window

import SparkApi
import tkinter as tk

# 以下密钥信息从控制台获取
appid = "2b7ab044"  # 填写控制台中获取的 APPID 信息
api_secret = "YTFiNmEzZTZmZTk3MGJhYzNkODIwZDc3"  # 填写控制台中获取的 APISecret 信息
api_key = "fd769aa40b92619985003c8000298d22"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
domain = "general"  # v1.5版本
# domain = "generalv2"  # v2.0版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

text = []


# 获取消息长度
def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


# 检查消息长度，控制在8000以内
def checklen(text):
    while getlength(text) > 8000:
        del text[0]
    return text


# 获取消息内容
def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


if __name__ == '__main__':

    # 全局变量
    answer = ""
    question = []


    # 发送问题的函数
    def send_question():
        global answer, question
        user_input = entry.get()  # 获取用户输入的问题
        question.append({"role": "user", "content": user_input})
        SparkApi.answer = ""  # 清空答案
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)  # 发送问题
        question.pop()  # 移除已发送的问题
        entry.delete(0, tk.END)  # 清空用户输入
        update_answer()

        # question = checklen(getText("user", entry.get()))   # 获取用户输入的问题
        # SparkApi.answer = ""  # 清空答案
        # entry.delete(0, tk.END)  # 清空用户输入
        # SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)  # 发送问题
        # getText("assistant", SparkApi.answer)  # 存储回答
        # text.config(state=tk.NORMAL)
        # text.insert(tk.END, f"\n星火: {SparkApi.content}\n")  # 在文本框中显示答案
        # text.config(state=tk.DISABLED)
        # text.see(tk.END)  # 将滚动条移动到最后显示最新的答案


    # 更新答案文本框
    def update_answer():
        global answer
        # text.delete("1.0", tk.END)  # 清空文本框内容
        if SparkApi.answer != answer:  # 检查是否有新的答案
            answer = SparkApi.answer
            text.config(state=tk.NORMAL)
            text.insert(tk.END, f"\n星火: {answer}\n")  # 在文本框中显示答案
            text.config(state=tk.DISABLED)
            text.see(tk.END)  # 将滚动条移动到最后显示最新的答案


    # 主窗口

    root = tk.Tk()
    root.title("7#401自己的miniChatGPT")
    # 设置窗体图标
    from icon import img

    # 读取base64转码后的数据，并设置压缩图标
    picture = open("picture.ico", "wb+")
    picture.write(base64.b64decode(img))
    picture.close()
    root.iconbitmap('picture.ico')
    os.remove("picture.ico")

    # 创建文本框用于显示回答
    text = tk.Text(root, height=20, width=50, state=tk.DISABLED)
    text.pack()

    # # 创建滚动条
    # scrollbar = tk.Scrollbar(root)
    # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    # scrollbar.config(command=text.yview)

    # 创建文本框用于用户输入问题
    entry = tk.Entry(root, width=50)
    entry.pack()

    # 创建发送按钮
    send_button = tk.Button(root, text="发送", command=send_question)
    send_button.pack()

    # 更新答案
    # update_answer()

    # 运行主循环
    root.mainloop()
