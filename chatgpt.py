import openai
import json
import os
from openai.error import AuthenticationError,InvalidRequestError,APIConnectionError,RateLimitError
from record import Recorder
from voice import Voice

# 获取 api
def get_api_key():
    openai_key_file = './openaikey.json'
    while True:
        try:
            with open(openai_key_file, 'r', encoding='utf-8') as f:
                openai_key = json.loads(f.read())
        except FileNotFoundError:
            openai_key = {"api": input("请输入API密钥：")}
            with open(openai_key_file, 'w', encoding='utf-8') as f:
                json.dump(openai_key, f)

        # 验证 API 密钥是否有效
        openai.api_key = openai_key['api']
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt="Hello,",
                max_tokens=1
            )
            print("密钥校验成功！")
            break  # API 密钥有效，跳出循环
        except AuthenticationError:
            print("API 密钥无效，请重新输入")
        except APIConnectionError:
            print("无法连接，请检查网络")
        except RateLimitError:
            print("密钥已经超出使用限制，请更换")


        # 更新 API 密钥并写入文件
        openai_key = {"api": input("请输入API密钥：")}
        with open(openai_key_file, 'w', encoding='utf-8') as f:
            json.dump(openai_key, f)

    return openai_key['api']

class ChatGPT:
    def __init__(self, user):
        self.user = user
        self.messages = [{"role": "system", "content": ""}]
        self.filename = f"./logs/{self.user}_messages.json"
        self.tokens = 0
        ''' 弃用代码,本代码虽然可以统计tokens，但是无法实现打字机效果
    def ask_gpt(self):
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            #设置最大返回的tokens，便于控制。
            max_tokens = 500
        )
        self.tokens = rsp['usage']['total_tokens']
        print(self.tokens)
        return rsp.get("choices")[0]["message"]["content"]
        '''
    def ask_gpt(self):
        rsp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.messages,
            max_tokens=500,
            stream=True
        )
        text = ''
        print("【chatgpt】",end='')
        for chunk in rsp:
            if 'choices' in chunk:
                if 'content' in chunk['choices'][0]['delta']:
                    text += chunk['choices'][0]["delta"]["content"]
                    print(chunk['choices'][0]['delta']['content'], end='')
            if 'finish_reason' in chunk and chunk['finish_reason'] == 'stop':
                break
        return text

    def load_history(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                # 只读取最近的15条记录
                self.messages = json.loads(content).get(self.user, [])[-15:]
        except Exception as e:
            print("读取历史记录出错：", e)

    def clear_history(self):
        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)
                print("历史记录已清除！")
        except Exception as e:
            print("清除历史记录出错：", e)

    def writeTojson(self):
        try:
            # 判断文件是否存在
            if not os.path.exists(self.filename):
                with open(self.filename, "w") as f:
                    # 创建文件
                    pass
            # 读取
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                msgs = json.loads(content) if len(content) > 0 else {}
            # 追加
            msgs.update({self.user: self.messages})
            # 写入
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(msgs, f)
        except Exception as e:
            print(f"错误代码：{e}")


def main():
    openai.api_key = get_api_key()
    user = input("请输入用户名称: ")
    chat = ChatGPT(user)
    if os.path.exists(f"./logs/{user}_messages.json"):
        # 提示用户是否要载入历史记录
        load_history = input("查询到历史记录。是否要载入历史记录？（输入yes或no）：")
        if load_history.lower() == "yes":
            chat.load_history()

    # 循环
    while 1:
        try:
            # 语音识别模块在这里
            Detect = Recorder.record_utils()
            if Detect == False:
                break
            output = Voice.transcribe_audio()
            if output == "停止对话" or output == "停止對話":
                chat.writeTojson()
                print("*******保存退出*******")
                break
            if output == "清除记录" or output == "清除記錄":
                chat.clear_history()
                print("*******历史记录已清除*******")
                user = input("请输入用户名称: ")
                chat = ChatGPT(user)
                continue

            print(f"\n【{chat.user}】" + output)

            #q = input(f"\n【{chat.user}】")

            # 提问，聊天记录更新
            q = output
            chat.messages.append({"role": "user", "content": q})
            answer = chat.ask_gpt()
            chat.messages.append({"role": "assistant", "content": answer})
            chat.writeTojson()
        except InvalidRequestError:
            print("总对话字数超出限制，请重试")
            #超出限制后会清掉聊天记录，忽略本次，并重新读取前15条聊天记录
            chat.messages.clear()
            chat.load_history()
        except APIConnectionError:
            print("无法连接，请检查网络")
        except RateLimitError:
            print("密钥已经超出使用限制，请更换")


if __name__ == '__main__':
    main()
