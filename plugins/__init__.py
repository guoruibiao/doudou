#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
插件系统基类
"""


class BasePlugin:
    """
    插件基类，所有插件都应该继承这个类
    """
    
    # 插件名称，子类必须定义
    plugin_name = "BasePlugin"
    
    # 插件描述
    plugin_description = "基础插件类"
    
    # 优先级，数字越大优先级越高
    priority = 0
    
    def can_handle(self, user_input, context_manager):
        """
        检查是否可以处理用户输入
        
        Args:
            user_input: 用户输入的文本
            context_manager: 上下文管理器实例
            
        Returns:
            bool: 是否可以处理
        """
        # 默认返回True，表示可以处理所有输入
        # 子类可以重写此方法来实现更精确的判断
        return True
    
    def handle(self, user_input, context_manager):
        """
        处理用户输入并生成响应
        
        Args:
            user_input: 用户输入的文本
            context_manager: 上下文管理器实例
            
        Returns:
            str: 响应文本，如果返回None表示不处理此输入
        """
        # 子类必须实现此方法
        raise NotImplementedError("子类必须实现handle方法")
    
    def initialize(self):
        """
        插件初始化方法，在插件加载时调用
        """
        pass
    
    def cleanup(self):
        """
        插件清理方法，在插件卸载时调用
        """
        pass