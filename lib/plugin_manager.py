#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
插件管理器类
"""

import os
import importlib.util
import inspect
from config.config import PLUGINS_DIR, ENABLED_PLUGINS


class PluginManager:
    """
    插件管理器，负责加载、管理和执行插件
    """
    
    def __init__(self):
        """
        初始化插件管理器
        """
        self.plugins = []  # 加载的插件列表
        self._load_plugins()
    
    def _load_plugins(self):
        """
        加载插件目录中的所有插件
        """
        # 确保插件目录存在
        if not os.path.exists(PLUGINS_DIR):
            os.makedirs(PLUGINS_DIR)
            return
        
        # 遍历插件目录
        for idx, plugin_name in enumerate(os.listdir(PLUGINS_DIR)):
            plugin_path = os.path.join(PLUGINS_DIR, plugin_name)

            # 跳过非目录项和以_开头的目录
            if not os.path.isdir(plugin_path) or plugin_name.startswith('_'):
                continue
            
            # 检查是否在启用列表中
            if ENABLED_PLUGINS and plugin_name not in ENABLED_PLUGINS:
                continue
            
            # 查找主插件文件
            main_file = os.path.join(plugin_path, '__init__.py')
            if not os.path.exists(main_file):
                print(f"警告: 插件 {plugin_name} 缺少 __init__.py 文件")
                continue
            
            try:
                # 动态导入插件
                spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}", main_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 查找插件类
                plugin_class = None
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and hasattr(obj, 'plugin_name') and
                            hasattr(obj, 'handle') and obj.plugin_name != "BasePlugin"):
                        plugin_class = obj
                        break

                
                if plugin_class:
                    # 实例化插件
                    plugin = plugin_class()
                    # 获取优先级，默认为0, 按照配置中的优先级顺序进行赋值处理
                    priority = getattr(plugin, 'priority', 0)
                    if priority == 0:
                        priority = idx
                    # 添加到插件列表
                    self.plugins.append((priority, plugin))
                    # print(f"成功加载插件: {plugin_name}")
                else:
                    print(f"警告: 插件 {plugin_name} 中未找到有效的插件类")
                    
            except Exception as e:
                print(f"加载插件 {plugin_name} 失败: {e}")
        
        # 按优先级排序插件，优先级高的先执行
        self.plugins.sort(key=lambda x: x[0], reverse=True)
        print("插件优先级如下：", self.plugins)
    
    def process_input(self, user_input, context_manager):
        """
        处理用户输入，通过插件进行响应
        
        Args:
            user_input: 用户输入的文本
            context_manager: 上下文管理器实例
            
        Returns:
            str: 插件生成的响应文本，如果没有插件处理则返回None
        """
        for _, plugin in self.plugins:
            try:
                # 检查插件是否可以处理该输入
                if hasattr(plugin, 'can_handle'):
                    if not plugin.can_handle(user_input, context_manager):
                        continue
                
                # 调用插件的处理方法
                response = plugin.handle(user_input, context_manager)
                if response:
                    return response
            except Exception as e:
                print(f"插件 {getattr(plugin, 'plugin_name', 'unknown')} 执行错误: {e}")
        
        # 没有插件处理
        return None
    
    def reload_plugins(self):
        """
        重新加载所有插件
        """
        self.plugins = []
        self._load_plugins()
        print(f"重新加载完成，当前加载了 {len(self.plugins)} 个插件")
    
    def get_plugin_info(self):
        """
        获取所有已加载插件的信息
        
        Returns:
            list: 插件信息列表
        """
        plugin_info = []
        for priority, plugin in self.plugins:
            plugin_info.append({
                'name': getattr(plugin, 'plugin_name', 'unknown'),
                'description': getattr(plugin, 'plugin_description', '无描述'),
                'priority': priority
            })
        return plugin_info