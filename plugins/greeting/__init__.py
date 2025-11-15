#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
问候插件
"""

import random
from plugins import BasePlugin


class GreetingPlugin(BasePlugin):
    """
    问候插件，用于回应用户的问候语
    """
    
    plugin_name = "GreetingPlugin"
    plugin_description = "回应用户的问候语"
    priority = 0  # 设置较高的优先级
    
    def __init__(self):
        """
        初始化问候插件
        """
        # 问候语列表
        self.greetings = [
            "你好！",
            "你好，有什么我可以帮助你的吗？",
            "嗨！很高兴为你服务。",
            "你好啊！",
            "你好，我在这里。"
        ]
        
        # 感谢语列表
        self.thanks = [
            "不客气！",
            "很高兴能帮到你！",
            "随时为你服务！",
            "不用谢！",
            "这是我应该做的。"
        ]
        
        # 再见语列表
        self.goodbyes = [
            "再见！",
            "下次见！",
            "祝你有愉快的一天！",
            "回头见！",
            "再见，有需要随时叫我。"
        ]
        
        # 问候关键词
        self.greeting_keywords = ["你好", "嗨", "喂", "哈喽", "早上好", "晚上好", "中午好"]
        
        # 感谢关键词
        self.thanks_keywords = ["谢谢", "感谢", "非常感谢", "多谢"]
        
        # 再见关键词
        self.goodbye_keywords = ["再见", "拜拜", "回头见", "下次见"]
    
    def can_handle(self, user_input, context_manager):
        """
        检查是否可以处理用户输入
        
        Args:
            user_input: 用户输入的文本
            context_manager: 上下文管理器实例
            
        Returns:
            bool: 是否可以处理
        """
        user_input = user_input.lower()
        
        # 检查是否包含问候关键词
        for keyword in self.greeting_keywords:
            if keyword in user_input:
                return True
        
        # 检查是否包含感谢关键词
        for keyword in self.thanks_keywords:
            if keyword in user_input:
                return True
        
        # 检查是否包含再见关键词
        for keyword in self.goodbye_keywords:
            if keyword in user_input:
                return True
        
        return False
    
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
        
        # 检查是否包含问候关键词
        for keyword in self.greeting_keywords:
            if keyword in user_input:
                response = random.choice(self.greetings)
                context_manager.add_context(user_input, response)
                return response
        
        # 检查是否包含感谢关键词
        for keyword in self.thanks_keywords:
            if keyword in user_input:
                response = random.choice(self.thanks)
                context_manager.add_context(user_input, response)
                return response
        
        # 检查是否包含再见关键词
        for keyword in self.goodbye_keywords:
            if keyword in user_input:
                response = random.choice(self.goodbyes)
                context_manager.add_context(user_input, response)
                return response
        
        return None