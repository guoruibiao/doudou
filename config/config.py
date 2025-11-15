#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
语音助手配置文件
"""

import os
import shutil
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# 唤醒词配置
WAKE_WORD_MODEL = "models/porcupine_params_zh.pv"  # 唤醒词模型路径
#WAKE_KEYWORD_PATHS = "models/豆豆_zh_mac_v3_0_0.ppn"  # 唤醒词模型路径
WAKE_KEYWORD_PATHS = "models/zh_raspberry-pi_v3_0_0.ppn"
KEYWORD_PATHS = ['']
SENSITIVITY = [0.5]  # 唤醒灵敏度（0.0-1.0）

# 语音识别模型；下载中文模型：https://alphacephei.com/vosk/models
#VOSK_MODEL = "models/vosk-model-small-cn-0.22"
VOSK_MODEL = "models/vosk-model-cn-0.22"

# 音频配置
AUDIO_DEVICE_INDEX = None  # 录音设备索引，None表示使用默认设备
SAMPLE_RATE = 16000  # 采样率
CHANNELS = 1  # 声道数
WAV_FILE_PATH = "/tmp/output.wav"

# 语音识别配置
DEFAULT_LANGUAGE = "zh-CN"  # 默认语言
RECOGNITION_TIMEOUT = 5  # 语音识别超时时间（秒）

# LLM 模型
LLM_HOST = os.getenv("LLM_HOST", "http://localhost:11434")
LLM_REQUEST_TIMEOUT = 90
LLM_MODEL_NAME = "gemma3" # qwen3 gemma3 deepseek-r1:8b

# 插件配置
PLUGINS_DIR = "plugins"  # 插件目录
ENABLED_PLUGINS = ["time", "weather", "greeting", "llm"]  # 默认启用的插件(顺序越靠前，优先级越高，越优先被响应)

# 上下文配置
CONTEXT_TIMEOUT = 120  # 上下文保持时间（秒）
MAX_CONTEXT_HISTORY = 10  # 最大历史上下文数量

# 日志配置
LOG_LEVEL = "INFO"  # 日志级别
LOG_FILE = "logs/assistant.log"  # 日志文件路径

# API配置（从环境变量读取）
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "")

# 创建必要的目录
os.makedirs("resources/models", exist_ok=True)
os.makedirs("logs", exist_ok=True)
TTS_TO_SPEECH_TMP_DIR = "tmp"
TTS_TO_SPEECH_FILENAME = "speech.mp3"
if os.path.exists(TTS_TO_SPEECH_TMP_DIR):
    shutil.rmtree(TTS_TO_SPEECH_TMP_DIR)
os.makedirs(TTS_TO_SPEECH_TMP_DIR, exist_ok=True)

# 默认音色以及可用音色列表
TTS_ENGINE_ROLE_DEFAULT    = "zh-CN-XiaoyouNeural"
TTS_ENGINE_ROLE_XIAOXIAO   = "zh-CN-XiaoxiaoNeural",      # 默认，自然; 晓晓（女）
TTS_ENGINE_ROLE_XIAOCHEN   = "zh-CN-XiaochenNeural",      # 温和; 晓晨（女）
TTS_ENGINE_ROLE_XIAOHAN    = "zh-CN-XiaohanNeural",       # 活泼; 晓涵（女）
TTS_ENGINE_ROLE_XIAOMENG   = "zh-CN-XiaomengNeural",      # 可爱; 晓梦（女）
TTS_ENGINE_ROLE_XIAOQIU    = "zh-CN-XiaoqiuNeural",       # 成熟; 晓秋（女）
TTS_ENGINE_ROLE_YUNYANG    = "zh-CN-YunyangNeural",       # 新闻播报; 云扬（男）
TTS_ENGINE_ROLE_YUNXI      = "zh-CN-YunxiNeural",         # 年轻男性; 云希（男）
TTS_ENGINE_ROLE_YUNJIAN    = "zh-CN-YunjianNeural",       # 沉稳; 云健（男）
TTS_ENGINE_ROLE_XIAORUI    = "zh-CN-XiaoruiNeural",       # 温和男性; 晓睿（男）
TTS_ENGINE_ROLE_XIAOSHUANG = "zh-CN-XiaoshuangNeural",    # 儿童音; 晓双（女）
TTS_ENGINE_ROLE_XIAOYAN    = "zh-CN-XiaoyanNeural",       # 专业; 晓颜（女）
TTS_ENGINE_ROLE_XIAOYOU    = "zh-CN-XiaoyouNeural",       # 儿童音; 晓悠（女）
