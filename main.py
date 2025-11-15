#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Doudou 语音助手主程序
"""
import os
import wave
import struct
import datetime
import logging
import pvporcupine
import config.config
from pvrecorder import PvRecorder
from lib.stt import SpeechToText, AdvancedVAD
from lib.tts import text_to_speech
from lib.plugin_manager import PluginManager
from lib.context_manager import ContextManager
from lib.ollama import OllamaClient
from config.config import LOG_LEVEL, LOG_FILE


# 配置日志
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DoudouAssistant')


class Assistant:
    """
    语音助手主类
    """
    
    def __init__(self):
        """
        初始化语音助手
        """
        logger.info("正在初始化Doudou语音助手...")
        
        # 初始化各组件
        # self.text_to_speech = TextToSpeech()
        self.context_manager = ContextManager()
        self.plugin_manager = PluginManager()
        self.vad_system = AdvancedVAD()
        self.stt = SpeechToText()

        # 初始化热词器
        self._init_porcupine()
        
        # 运行状态
        self.running = False
        
        logger.info("Doudou语音助手初始化完成")


    def _init_porcupine(self):
        try:
            # self.porcupine = pvporcupine.create(
            #     access_key=config.config.PORCUPINE_ACCESS_KEY,
            #     keywords=['porcupine'],
            #     # TODO 添加其他的参数信息
            #     # library_path=None,
            #     # model_path=None,
            #     # keyword_paths=config.config.KEYWORD_PATHS,
            #     # sensitivities=config.config.SENSITIVITY,
            # )
            self.porcupine = pvporcupine.create(
                access_key=config.config.PORCUPINE_ACCESS_KEY,
                model_path=config.config.WAKE_WORD_MODEL,
                keyword_paths=[config.config.WAKE_KEYWORD_PATHS],
                sensitivities=config.config.SENSITIVITY,
            )
        except pvporcupine.PorcupineInvalidArgumentError as e:
            print("One or more arguments provided to Porcupine is invalid: ", e)
            raise e
        except pvporcupine.PorcupineActivationError as e:
            print("AccessKey activation error")
            raise e
        except pvporcupine.PorcupineActivationLimitError as e:
            print("AccessKey '%s' has reached it's temporary device limit" % config.config.PORCUPINE_ACCESS_KEY)
            raise e
        except pvporcupine.PorcupineActivationRefusedError as e:
            print("AccessKey '%s' refused" % config.config.PORCUPINE_ACCESS_KEY)
            raise e
        except pvporcupine.PorcupineActivationThrottledError as e:
            print("AccessKey '%s' has been throttled" % config.config.PORCUPINE_ACCESS_KEY)
            raise e
        except pvporcupine.PorcupineError as e:
            print("Failed to initialize Porcupine")
            raise e

        # 初始化recoder
        self.recorder = PvRecorder(
            frame_length=self.porcupine.frame_length,
            device_index=-1) # 使用默认设备
        self.recorder.start()
        self.wav_file = None
        if config.config.WAV_FILE_PATH is not None:
            self.wav_file = wave.open(config.config.WAV_FILE_PATH, "w")
            self.wav_file.setnchannels(1)
            self.wav_file.setsampwidth(2)
            self.wav_file.setframerate(16000)

    
    def on_wake_word_detected(self):
        """
        唤醒词检测到后的处理函数
        """
        logger.info("检测到唤醒词，开始交互")
        
        # 在模拟模式下，直接打印提示信息而不是播放语音
        text_to_speech("豆豆在呢，咋了呀：")
        
        try:
            # 录音
            audio_filename = self.vad_system.record_until_silence(
                callback=None,
                max_duration=10,
            )
            # 语音识别
            user_input = self.stt.speech_to_text_by_vosk(audio_filename)
            # TODO 无法使用Google 服务时用vosk模型替代
            # user_input = self.stt.speech_to_text(audio_filename)
            # if user_input == "":
            #     user_input = self.stt.speech_to_text_by_vosk(audio_filename)
            print("user_input=", user_input)
            text_to_speech("已收到您的问题，让豆豆先思考下再回复您")

            # 检查上下文是否超时
            if self.context_manager.check_timeout():
                logger.info("上下文已超时，重新开始对话")
            
            # 通过插件处理输入
            response = self.plugin_manager.process_input(user_input, self.context_manager)

            # 删除创建的音频文件
            if os.path.exists(audio_filename):
                os.remove(audio_filename)

            
            if response:
                # 在模拟模式下，直接打印响应
                print(f"\n[助手] {response}")
                # 尝试播放语音响应
                try:
                    text_to_speech(response)
                except Exception as e:
                    logger.warning(f"语音播放失败: {e}")
            else:
                # 没有插件处理，给出默认回复
                default_response = "抱歉，我不太明白你的意思"
                print(f"\n[助手] {default_response}")
                try:
                    text_to_speech(default_response)
                except Exception as e:
                    logger.warning(f"语音播放失败: {e}")
                self.context_manager.add_context(user_input, default_response)

            # 打印日志
            logger.info(f"用户输入：{user_input}，助理回复：{response}")
                
        except Exception as e:
            logger.error(f"交互过程出错: {e}")
            error_response = "抱歉，处理时出现错误，请重试"
            print(f"\n[助手] {error_response}")
            try:
                text_to_speech(error_response)
            except Exception as e:
                logger.warning(f"语音播放失败: {e}")
    
    def start(self):
        """
        启动语音助手
        """
        if self.running:
            logger.warning("语音助手已经在运行")
            return
        
        self.running = True
        logger.info("语音助手启动")
        
        # 启动音频助手检测器
        try:
            while True:
                pcm = self.recorder.read()
                result = self.porcupine.process(pcm)

                if self.wav_file is not None:
                    self.wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                if result >= 0:
                    print('[%s] Detected %s' % (str(datetime.datetime.now()), result))
                    print("请说话，三秒后不说话即认为停止")
                    self.on_wake_word_detected()
        except KeyboardInterrupt:
            logger.info("用户中断程序")
        finally:
            self.stop()
    
    def stop(self):
        """
        停止语音助手
        """
        if not self.running:
            return
        
        self.running = False
        logger.info("语音助手停止")

        self.recorder.delete()
        self.porcupine.delete()
        if self.wav_file is not None:
            self.wav_file.close()
        
        # 清理资源
        del self.context_manager
        del self.plugin_manager

    def get_status(self):
        """
        获取语音助手状态
        
        Returns:
            dict: 状态信息
        """
        return {
            'running': self.running,
            'plugins': self.plugin_manager.get_plugin_info(),
            'context_count': len(self.context_manager.get_recent_contexts())
        }


def main():
    """
    主函数
    """
    print("="*60)
    print("欢迎使用 Doudou 语音助手（模拟模式）")
    print("="*60)
    print("\n使用说明:")
    print("  - 语音唤醒词检测")
    print("  - 录音后，识别音频内容并完成回复")
    print("  - 按 Ctrl+C 退出程序")
    print("="*60)
    
    assistant = Assistant()
    try:
        # 启动语音助手
        assistant.start()
        
    except KeyboardInterrupt:
        print("\n正在退出...")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        assistant.stop()
        print("程序已退出")


if __name__ == "__main__":
    main()