"""
Plugin System for Autonomous UI Engine
Phase 6: Innovation

Complete plugin system with lifecycle management, hooks, and registry.
"""

from .plugin_base import BasePlugin, PluginMetadata, PluginContext, PluginState
from .plugin_manager import PluginManager
from .registry import PluginRegistry, get_plugin_registry
from .hooks import HookManager, get_hook_manager, hook, before, after, Events

__all__ = [
    'BasePlugin',
    'PluginMetadata',
    'PluginContext',
    'PluginState',
    'PluginManager',
    'PluginRegistry',
    'get_plugin_registry',
    'HookManager',
    'get_hook_manager',
    'hook',
    'before',
    'after',
    'Events',
]
