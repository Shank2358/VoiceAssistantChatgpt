import pyaudio
import time
import threading
import wave
import numpy as np




# 定义类
class Recorder:

    def __init__(self, chunk=1024, channels=1, rate=64000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    # 定义开始录音
    def start(self):
        threading._start_new_thread(self.__recording, ())

    # 定义录音
    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while self._running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    # 定义停止
    def stop(self):
        self._running = False

    # 定义保存
    def save(self, filename):

        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        #print("Saved")

    def record_utils():
        # 这个值约等于0.5s，但是具体0.5s是多少RATE块我还不清楚，如果有明白的可以帮忙改一下
        RATE = 883500
        rec = Recorder()
        begin = time.time()
        print("\n开始录制")
        time.sleep(0.1)
        rec.start()

        # 添加计时器，每隔RATE秒钟计算一次音量
        rate_cnt = 0
        volume_list = []
        while True:
            if len(rec._frames) > 0:
                # 将最新的音频数据转换为numpy数组
                data = np.frombuffer(rec._frames[-1], dtype=np.int16)

                # 将音频数据分割成若干个长度为RATE的数据块
                for i in range(0, len(data), RATE):
                    rate_cnt += 1
                    if rate_cnt == RATE:
                        # 计算音量均值（绝对值）
                        volume = np.mean(np.abs(data[i:i + RATE]))

                        # 输出音量值
                        #print("当前音量：", volume)

                        # 将音量值加入列表
                        volume_list.append(volume)
                        #print(volume_list)

                        # 如果音量低于阈值，则停止录音
                        if len(volume_list) >= 6 and all(v < 200 for v in volume_list[-6:]):
                            #print("连续3秒音量低于200，自动停止录音")
                            rec.stop()
                            fina = time.time()
                            t = fina - begin
                            print('录音时间为%.2f秒' % t)
                            rec.save("./record/audio.wav")
                            if len(volume_list) <= 6:
                                #print("完全没有声音输入")
                                return False
                            else:
                                #print("还是有点声音输入的")
                                return True

                        # 重置计时器和音量列表
                        rate_cnt = 0





if __name__ == "__main__":
    Recorder.record_utils()
