import os.path
import time
import wave
import vosk
import json
import pyaudio
import numpy as np
import speech_recognition as sr
import config.config


class AdvancedVAD:
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.audio = pyaudio.PyAudio()

        # VAD参数
        self.energy_threshold = 300  # 能量阈值
        self.silence_limit = 3  # 静音限制（秒）
        self.previous_energy = 0
        self.energy_delta = 100  # 能量变化阈值

        # 状态
        self.is_recording = False
        self.recording_started = False

    def calculate_energy(self, data):
        """计算音频能量"""
        audio_data = np.frombuffer(data, dtype=np.int16)
        if len(audio_data) == 0:
            return 0
        return np.mean(np.abs(audio_data))

    def is_speech(self, data):
        """检测是否为语音"""
        energy = self.calculate_energy(data)

        # 基于能量和能量变化的语音检测
        is_above_threshold = energy > self.energy_threshold
        has_energy_change = abs(energy - self.previous_energy) > self.energy_delta

        self.previous_energy = energy

        return is_above_threshold or has_energy_change

    def record_until_silence(self, callback=None, max_duration=10):
        """录制直到检测到3秒静音"""
        self.is_recording = True
        self.recording_started = False

        audio_buffer = []
        silence_frames = 0
        speech_frames = 0

        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        print("🎤 等待语音开始...")

        try:
            while self.is_recording:
                data = stream.read(self.chunk, exception_on_overflow=False)

                if self.is_speech(data):
                    if not self.recording_started:
                        print("🗣️ 检测到语音，开始录制...")
                        self.recording_started = True

                    audio_buffer.append(data)
                    silence_frames = 0
                    speech_frames += 1

                else:
                    if self.recording_started:
                        silence_frames += 1
                        audio_buffer.append(data)  # 仍然保存静音帧

                # 检查停止条件
                silence_seconds = silence_frames * self.chunk / self.rate
                total_seconds = len(audio_buffer) * self.chunk / self.rate

                # 如果已经开始录制且检测到3秒静音，停止
                if self.recording_started and silence_seconds >= self.silence_limit:
                    print(f"检测到{silence_seconds:.1f}秒静音，停止录制")
                    break

                # 最大录制时长保护
                if total_seconds >= max_duration:
                    print("达到最大录制时长，停止录制")
                    break

        except Exception as e:
            print(f"录制错误: {e}")

        finally:
            stream.stop_stream()
            stream.close()

            filename = os.path.join(config.config.TTS_TO_SPEECH_TMP_DIR, f"command_{int(time.time())}.wav")
            if audio_buffer and self.recording_started:
                self.save_audio(audio_buffer, filename)
                print(f"✅ 录制完成: {filename}")

                if callback:
                    callback(filename)
            else:
                print("❌ 没有检测到有效语音")
            return filename

    def save_audio(self, frames, filename):
        """保存音频文件"""
        import wave

        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()


class SpeechToText:
    """语音转文本类"""

    @staticmethod
    def speech_to_text(audio_file):
        """使用SpeechRecognition进行语音识别"""
        try:
            r = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                # 调整环境噪声
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.record(source)

            # 使用Google语音识别
            text = r.recognize_google(audio, language='zh-CN')
            return text

        except ImportError:
            print("请安装SpeechRecognition: pip install SpeechRecognition")
            return ""
        except Exception as e:
            print(f"语音识别失败: {e}")
            return ""

    @staticmethod
    def speech_to_text_by_vosk(audio_file, model_path=config.config.VOSK_MODEL):
        """使用Vosk离线识别"""
        model = vosk.Model(model_path)
        wf = wave.open(audio_file, "rb")

        recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                results.append(result.get('text', ''))

        final_result = json.loads(recognizer.FinalResult())
        results.append(final_result.get('text', ''))

        return ' '.join(results)


# 集成到热词系统
def integrate_with_hotword():
    """集成到热词检测系统"""
    vad_system = AdvancedVAD()
    stt = SpeechToText()

    def hotword_callback():
        """热词检测回调"""
        print("🔥 热词唤醒！")
        vad_system.record_until_silence(callback=process_command)

    def process_command(audio_file):
        """处理指令"""
        command_text = stt.speech_to_text(audio_file)
        if command_text:
            print(f"🎯 指令: {command_text}")
            # 执行相应操作

    return hotword_callback


# if __name__ == "__main__":
#     vad_system = AdvancedVAD()
#     stt = SpeechToText()
#     audio_file = vad_system.record_until_silence()
#     print("audio_file:", audio_file)
#     ret = stt.speech_to_text_by_vosk(audio_file)
#     print("ret:", ret)