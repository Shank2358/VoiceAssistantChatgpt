import openai
import json
from record import Recorder

class Voice:
    def get_api_key():
        # 可以自己根据自己实际情况实现
        # 以我为例子，我是存在一个 openai_key 文件里，json 格式
        '''
        {"api": "你的 api keys"}
        '''
        openai_key_file = './openaikey.json'
        with open(openai_key_file, 'r', encoding='utf-8') as f:
            openai_key = json.loads(f.read())
        return openai_key['api']



    def transcribe_audio():#转换用
        file_path = "./record/audio.wav"
        # 使用openAI api
        with open(file_path, "rb") as f:
            result = openai.Audio.transcribe("whisper-1", f)
        transcript = result["text"]
        #print("Transcript:", transcript)
        return transcript

if __name__ == "__main__":
    openai.api_key = Voice.get_api_key()
    Recorder.record_utils()
    Voice.transcribe_audio()