#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
问候插件
"""

import random

import config.config
from plugins import BasePlugin
from lib.ollama import OllamaClient


class LLMPlugin(BasePlugin):
    """
    问候插件，用于回应用户的问候语
    """

    plugin_name = "LLMPlugin"
    plugin_description = "调用大模型完成回答"
    priority = 0  # 设置较高的优先级

    def __init__(self):
        """
        初始化问候插件
        """
        self.prompt_template = """
        角色设定 
        你是一个名为【豆豆】的智能语音助手，专注于为用户提供高效、个性化、贴心的日常生活支持。你的核心目标是简化用户操作，提升生活品质，通过自然语言交互完成多样化任务。

        交互风格
        1. 解决问题要干脆利落，答案要直接明确，不要绕弯子，能够表达出含义的同时尽可能精简。
        2. 一定要幽默，说话得体，不要说教，保持贱萌但不油腻的调性
        3. 语言风格要带有强烈的猥琐感
        4. 语言风格要简洁明了，不要模糊不清，不拖泥带水
        5. 简单指令（如“打开客厅灯”“查明天天气”）秒回，不拖沓； 复杂任务（如“规划周末家庭出游”）先给第一步：“先搞定‘去哪玩’，咱是想找个能遛娃的公园，还是能啃烤串的夜市呀？”，让用户快速参与决策，不卡顿。

        请基于上述角色设定和语言交互风格，针对下面提出的这个问题进行作答：
        {}
        """
        self.client = OllamaClient(
            base_url=config.config.LLM_HOST,
            timeout=config.config.LLM_REQUEST_TIMEOUT,
        )

    def can_handle(self, user_input, context_manager):
        """
        检查是否可以处理用户输入

        Args:
            user_input: 用户输入的文本
            context_manager: 上下文管理器实例

        Returns:
            bool: 是否可以处理
        """
        # 使用大模型进行兜底处理
        return True

    def handle(self, user_input, context_manager):
        """
        处理用户输入并生成响应

        Args:
            user_input: 用户输入的文本
            context_manager: 上下文管理器实例

        Returns:
            str: 响应文本
        """
        user_input = user_input.lower()
        prompt = self.prompt_template.format(user_input)
        response = self.client.generate_text(config.config.LLM_MODEL_NAME, prompt)
        context_manager.add_context(user_input, response)
        return response
