#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
上下文管理工具类
"""

import time
from config.config import CONTEXT_TIMEOUT, MAX_CONTEXT_HISTORY


class Context:
    """
    上下文类，包含用户输入、系统响应和时间戳
    """
    
    def __init__(self, user_input, system_response=None):
        """
        初始化上下文
        
        Args:
            user_input: 用户输入的文本
            system_response: 系统的响应文本
        """
        self.user_input = user_input
        self.system_response = system_response
        self.timestamp = time.time()


class ContextManager:
    """
    上下文管理器，管理对话历史和上下文信息
    """
    
    def __init__(self):
        """
        初始化上下文管理器
        """
        self.context_history = []  # 上下文历史
    
    def add_context(self, user_input, system_response=None):
        """
        添加新的上下文
        
        Args:
            user_input: 用户输入的文本
            system_response: 系统的响应文本
        """
        # 创建新的上下文
        context = Context(user_input, system_response)
        # 添加到历史记录
        self.context_history.append(context)
        # 保持历史记录不超过最大数量
        if len(self.context_history) > MAX_CONTEXT_HISTORY:
            self.context_history = self.context_history[-MAX_CONTEXT_HISTORY:]
    
    def get_recent_contexts(self, max_count=None):
        """
        获取最近的上下文
        
        Args:
            max_count: 最大返回数量，None表示返回所有有效上下文
            
        Returns:
            list: 上下文列表
        """
        # 获取当前时间
        current_time = time.time()
        # 过滤有效上下文（未超时）
        valid_contexts = [
            ctx for ctx in self.context_history 
            if current_time - ctx.timestamp < CONTEXT_TIMEOUT
        ]
        
        # 如果指定了最大数量，只返回最近的max_count个
        if max_count and len(valid_contexts) > max_count:
            return valid_contexts[-max_count:]
        
        return valid_contexts
    
    def get_full_context_text(self):
        """
        获取完整的上下文文本，用于生成回复
        
        Returns:
            str: 上下文文本
        """
        contexts = self.get_recent_contexts()
        context_text = ""
        
        for ctx in contexts:
            context_text += f"用户: {ctx.user_input}\n"
            if ctx.system_response:
                context_text += f"助手: {ctx.system_response}\n"
        
        return context_text
    
    def clear_context(self):
        """
        清空上下文历史
        """
        self.context_history = []
    
    def check_timeout(self):
        """
        检查并清理超时的上下文
        
        Returns:
            bool: 是否所有上下文都已超时
        """
        current_time = time.time()
        # 过滤有效上下文
        self.context_history = [
            ctx for ctx in self.context_history 
            if current_time - ctx.timestamp < CONTEXT_TIMEOUT
        ]
        
        # 返回是否还有有效上下文
        return len(self.context_history) == 0