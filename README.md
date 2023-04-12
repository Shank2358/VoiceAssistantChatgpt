# VoiceAssistantChatgpt
一个语音交互输入的调用Chatgpt项目，你的python助理
# 使用准备
-   python3.10以上版本
-   申请 [OpenAI API Key](https://platform.openai.com/account/api-keys) 
-   能够连接上chatgptapi的网络



**[广告] 免费 OpenAI API Key**  
<img src=https://user-images.githubusercontent.com/50035229/229976556-99e8ac26-c8c3-4f56-902d-a52a7f2e50d5.png width=300px />  

[获取免费的OpenAI API Key](https://freeopenai.xyz/) 
# 安装
## Windows Installation
```powershell
git clone https://github.com/SnowfallC/VoiceAssistantChatgpt.git
cd VoiceAssistantChatgpt

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
```
# 启动
```powershell
.\venv\Scripts\activate
python chatgpt.py
```
或者run_chatgptAssistant.bat

# 使用指南
第一次登陆要求你输入api密钥，之后密钥会保存在openaikey.json中，如果需要修改在这里修改。每次运行程序时都会检查你的密钥是否能够连接上网络。

输入用户名称会保存该用户的全部聊天记录，不同的用户单独保存。下次可以手动输入yes或者no进行聊天记录的载入。

语音“停止对话”会保存退出程序。语音“清除记录”会清除掉聊天记录，回到输入用户名称的地方。

语音输入设置的是3秒内没有语音输入就停止程序，没有重新唤醒的能力。之后会继续完善。打字机效果在cmd中没有效果。使用pycharm或者Vscode可以预览到效果。

如果你有好的意见和建议，以及bug汇报，欢迎提出和Pull request。
# 更新日志
2023.4.12 程序上传

# 参考文档
[ChatGPT-3.5-API](https://github.com/XksA-me/ChatGPT-3.5-API)
