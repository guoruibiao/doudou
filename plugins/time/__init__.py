#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
时间插件
"""

import datetime
from plugins import BasePlugin


class TimePlugin(BasePlugin):
    """
    时间插件，用于回答用户关于时间的问题
    """
    
    plugin_name = "TimePlugin"
    plugin_description = "回答用户关于时间和日期的问题"
    priority = 0  # 设置较高的优先级
    
    def __init__(self):
        """
        初始化时间插件
        """
        # 时间相关关键词
        self.time_keywords = ["几点", "时间", "现在"]
        
        # 日期相关关键词
        self.date_keywords = ["日期", "几号", "星期", "今天"]
    
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
        
        # 检查是否包含时间关键词
        for keyword in self.time_keywords:
            if keyword in user_input:
                return True
        
        # 检查是否包含日期关键词
        for keyword in self.date_keywords:
            if keyword in user_input:
                return True
        
        # 检查是否包含特定的时间问题
        if "现在几点" in user_input or "现在时间" in user_input:
            return True
        
        if "今天几号" in user_input or "今天星期几" in user_input:
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
        now = datetime.datetime.now()
        
        # 获取当前时间
        current_time = now.strftime("%H:%M")
        
        # 获取当前日期
        week_days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        current_date = now.strftime("%Y年%m月%d日")
        current_weekday = week_days[now.weekday()]
        
        # 时间相关问题
        if any(keyword in user_input for keyword in self.time_keywords) or "几点" in user_input:
            response = f"现在是 {current_time}"
            context_manager.add_context(user_input, response)
            return response
        
        # 日期相关问题
        if "星期" in user_input:
            response = f"今天是 {current_weekday}"
            context_manager.add_context(user_input, response)
            return response
        
        if any(keyword in user_input for keyword in self.date_keywords) or "几号" in user_input:
            response = f"今天是 {current_date}，{current_weekday}"
            context_manager.add_context(user_input, response)
            return response
        
        return None