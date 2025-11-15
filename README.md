# Doudou 智能语音助手

一个基于Python的智能语音助手，支持语音唤醒、语音识别、自然语言处理和插件扩展功能。

## 功能特性

-  🎙️ 语音唤醒：支持自定义唤醒词
- ️ 语音识别：支持在线和离线两种识别模式
- 🔊 语音合成：支持多种音色选择
-  智能对话：集成LLM大语言模型
-  🔌 插件系统：可扩展的功能模块
-  ⏳ 上下文记忆：支持多轮对话

## 系统要求

- Python 3.8+
- macOS/Linux (Windows部分功能可能受限)
- 麦克风设备

## 安装部署

### 1. 克隆项目

```bash
git clone https://github.com/guoruibiao/doudou.git
cd doudou
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制.env.example为.env并填写你的API密钥：

```bash
cp .env.example .env
```

需要配置的密钥包括：
- Porcupine访问密钥(用于语音热词唤醒) 自行构建即可 https://picovoice.ai/

### 5. 下载模型文件

下载并放置以下模型文件到`models/`目录：

1. Vosk语音识别模型(中文):
   ```bash
   wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
   unzip vosk-model-cn-0.22.zip -d models/
   ```

2. snowboy已过时，本项目使用Porcupine唤醒词模型(已包含在项目中)，对于中文项目需要额外添加`porcupine_params_zh.pv`, 在porcupine官网自行训练触发词即可。

## 运行程序

```bash
python main.py
```

首次运行会自动创建必要的目录结构。

## 插件开发

项目支持通过插件扩展功能，插件位于`plugins/`目录。

### 创建新插件

1. 在`plugins/`下创建插件目录
2. 创建`__init__.py`文件并实现插件类
3. 在`config/config.py`的`ENABLED_PLUGINS`中添加插件名

插件模板：

```python
class MyPlugin:
    plugin_name = "myplugin"
    plugin_description = "我的插件描述"
    
    def can_handle(self, user_input, context_manager):
        # 判断是否能处理该输入
        return "关键词" in user_input
    
    def handle(self, user_input, context_manager):
        # 处理逻辑
        return "响应内容"
```

## 配置说明

主要配置文件`config/config.py`可调整：

- 唤醒词灵敏度
- 语音识别模型路径
- 默认语音音色
- 启用的插件列表
- 日志级别等

## 常见问题

### 唤醒不灵敏

调整`config/config.py`中的`SENSITIVITY`值(0-1之间)

### 语音识别不准

1. 检查麦克风是否正常工作
2. 尝试使用在线识别(需网络)
3. 确保Vosk模型文件完整

### 插件不生效

1. 检查插件目录结构是否正确
2. 确认插件名已添加到`ENABLED_PLUGINS`
3. 查看日志排查错误

## 项目结构

```
doudou/
├── config/        # 配置文件
├── lib/           # 核心功能模块
├── logs/          # 日志文件
├── models/        # AI模型文件
├── plugins/       # 插件目录
├── resources/     # 资源文件
├── tmp/           # 临时文件
├── .env           # 环境变量
└── main.py        # 主程序入口
```

## 贡献指南

欢迎提交Pull Request或Issue报告问题。