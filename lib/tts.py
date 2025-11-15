import os
import time
import edge_tts
import asyncio
import pygame
import pyttsx3

import config.config

"""
# 音色列表
"晓晓（女）": "zh-CN-XiaoxiaoNeural",      # 默认，自然
"晓晨（女）": "zh-CN-XiaochenNeural",      # 温和
"晓涵（女）": "zh-CN-XiaohanNeural",       # 活泼
"晓梦（女）": "zh-CN-XiaomengNeural",      # 可爱
"晓秋（女）": "zh-CN-XiaoqiuNeural",       # 成熟
"云扬（男）": "zh-CN-YunyangNeural",       # 新闻播报
"云希（男）": "zh-CN-YunxiNeural",         # 年轻男性
"云健（男）": "zh-CN-YunjianNeural",       # 沉稳
"晓睿（男）": "zh-CN-XiaoruiNeural",       # 温和男性
"晓双（女）": "zh-CN-XiaoshuangNeural",    # 儿童音
"晓颜（女）": "zh-CN-XiaoyanNeural",       # 专业
"晓悠（女）": "zh-CN-XiaoyouNeural",       # 儿童音
"""

def play_mp3_pygame(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # 等待播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# 组合使用示例
def text_to_speech(text, output_file=""):
    if output_file == "":
        output_file = os.path.join(config.config.TTS_TO_SPEECH_TMP_DIR, config.config.TTS_TO_SPEECH_FILENAME)
    try:
        # 尝试使用 Edge-TTS
        # raise "failed"
        asyncio.run(edge_tts.Communicate(
            text=text,
            voice=config.config.TTS_ENGINE_ROLE_DEFAULT,  # 音色
            rate="+2%",  # 语速
            pitch="+10Hz",  # 音调
            volume="+20%"  # 音量
        ).save(output_file))
        if os.path.exists(output_file):
            play_mp3_pygame(output_file)
        else:
            play_mp3_pygame(output_file)
        # print("使用在线TTS服务")
    except:
        # 失败时使用离线方案
        engine = pyttsx3.init()
        # 设置属性，例如语速和音量
        engine.setProperty('rate', 150)  # 语速，范围是0-400之间
        engine.setProperty('volume', 0.8)  # 音量，范围是0.0-1.0之间
        engine.say(text)
        engine.runAndWait()
        # print("使用离线TTS服务")

if __name__ == '__main__':
    text_to_speech("测试文案")
