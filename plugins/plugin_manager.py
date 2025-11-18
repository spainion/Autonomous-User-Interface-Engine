"""
Plugin Manager for Autonomous UI Engine
Phase 6: Innovation - Plugin System

Manages plugin lifecycle: load, unload, enable, disable, reload.
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

from .plugin_base import BasePlugin, PluginState, PluginContext
from .registry import PluginRegistry, get_plugin_registry
from .hooks import HookManager, get_hook_manager

logger = logging.getLogger(__name__)


class PluginManager:
    """
    Manages plugin lifecycle and coordination.
    """
    
    def __init__(
        self,
        app_instance: Any = None,
        plugin_directories: Optional[List[Path]] = None
    ):
        """
        Initialize the plugin manager.
        
        Args:
            app_instance: Reference to main application
            plugin_directories: List of directories containing plugins
        """
        self.app_instance = app_instance
        self.registry = get_plugin_registry()
        self.hook_manager = get_hook_manager()
        
        # Add plugin directories
        if plugin_directories:
            self.registry.plugin_directories.extend(plugin_directories)
        
        self._shared_data: Dict[str, Any] = {}
        
    async def load_plugin(
        self,
        plugin_name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Load a plugin.
        
        Args:
            plugin_name: Name of plugin to load
            config: Optional configuration for plugin
            
        Returns:
            True if load successful
        """
        try:
            # Get plugin registration
            registration = self.registry.get_plugin(plugin_name)
            if not registration:
                logger.error(f"Plugin {plugin_name} not found in registry")
                return False
            
            # Check if already loaded
            if self.registry.is_plugin_loaded(plugin_name):
                logger.warning(f"Plugin {plugin_name} already loaded")
                return True
            
            # Check dependencies
            satisfied, missing = self.registry.check_dependencies(plugin_name)
            if not satisfied:
                logger.error(
                    f"Cannot load {plugin_name}, missing dependencies: {missing}"
                )
                return False
            
            # Create plugin context
            context = PluginContext(
                app_instance=self.app_instance,
                config=config or {},
                shared_data=self._shared_data,
                logger=logger
            )
            
            # Instantiate plugin
            instance = registration.plugin_class(context)
            
            # Validate configuration
            if config and not instance.validate_config(config):
                logger.error(f"Invalid configuration for plugin {plugin_name}")
                return False
            
            # Call on_load lifecycle hook
            await instance.on_load()
            
            # Store instance
            registration.instance = instance
            self.registry._plugin_instances[plugin_name] = instance
            registration.load_count += 1
            
            logger.info(f"Loaded plugin: {plugin_name}")
            
            # Trigger hook
            await self.hook_manager.trigger("plugin.load", plugin_name=plugin_name)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            if registration:
                registration.last_error = str(e)
            return False
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin.
        
        Args:
            plugin_name: Name of plugin to unload
            
        Returns:
            True if unload successful
        """
        try:
            instance = self.registry.get_plugin_instance(plugin_name)
            if not instance:
                logger.warning(f"Plugin {plugin_name} not loaded")
                return False
            
            # Disable if enabled
            if instance.state == PluginState.ENABLED:
                await self.disable_plugin(plugin_name)
            
            # Call on_unload lifecycle hook
            await instance.on_unload()
            
            # Remove instance
            del self.registry._plugin_instances[plugin_name]
            registration = self.registry.get_plugin(plugin_name)
            if registration:
                registration.instance = None
            
            logger.info(f"Unloaded plugin: {plugin_name}")
            
            # Trigger hook
            await self.hook_manager.trigger("plugin.unload", plugin_name=plugin_name)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False
    
    async def enable_plugin(self, plugin_name: str) -> bool:
        """
        Enable a loaded plugin.
        
        Args:
            plugin_name: Name of plugin to enable
            
        Returns:
            True if enable successful
        """
        try:
            instance = self.registry.get_plugin_instance(plugin_name)
            if not instance:
                logger.error(f"Plugin {plugin_name} not loaded")
                return False
            
            if instance.state == PluginState.ENABLED:
                logger.warning(f"Plugin {plugin_name} already enabled")
                return True
            
            # Call on_enable lifecycle hook
            await instance.on_enable()
            
            logger.info(f"Enabled plugin: {plugin_name}")
            
            # Trigger hook
            await self.hook_manager.trigger("plugin.enable", plugin_name=plugin_name)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable plugin {plugin_name}: {e}")
            await instance.on_error(e)
            return False
    
    async def disable_plugin(self, plugin_name: str) -> bool:
        """
        Disable an enabled plugin.
        
        Args:
            plugin_name: Name of plugin to disable
            
        Returns:
            True if disable successful
        """
        try:
            instance = self.registry.get_plugin_instance(plugin_name)
            if not instance:
                logger.error(f"Plugin {plugin_name} not loaded")
                return False
            
            if instance.state == PluginState.DISABLED:
                logger.warning(f"Plugin {plugin_name} already disabled")
                return True
            
            # Call on_disable lifecycle hook
            await instance.on_disable()
            
            logger.info(f"Disabled plugin: {plugin_name}")
            
            # Trigger hook
            await self.hook_manager.trigger("plugin.disable", plugin_name=plugin_name)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable plugin {plugin_name}: {e}")
            return False
    
    async def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload a plugin (unload and load again).
        
        Args:
            plugin_name: Name of plugin to reload
            
        Returns:
            True if reload successful
        """
        logger.info(f"Reloading plugin: {plugin_name}")
        
        # Get current config
        instance = self.registry.get_plugin_instance(plugin_name)
        config = instance.context.config if instance else {}
        
        # Unload and load
        if await self.unload_plugin(plugin_name):
            return await self.load_plugin(plugin_name, config)
        
        return False
    
    async def execute_plugin(
        self,
        plugin_name: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute a plugin's main functionality.
        
        Args:
            plugin_name: Name of plugin to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Plugin execution result
        """
        instance = self.registry.get_plugin_instance(plugin_name)
        if not instance:
            raise ValueError(f"Plugin {plugin_name} not loaded")
        
        if instance.state != PluginState.ENABLED:
            raise ValueError(f"Plugin {plugin_name} not enabled")
        
        return await instance.execute(*args, **kwargs)
    
    async def load_all(self, configs: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, bool]:
        """
        Load all registered plugins.
        
        Args:
            configs: Optional dictionary of plugin configs
            
        Returns:
            Dictionary of plugin_name -> success status
        """
        results = {}
        configs = configs or {}
        
        for plugin_name in self.registry._registered_plugins.keys():
            config = configs.get(plugin_name)
            results[plugin_name] = await self.load_plugin(plugin_name, config)
        
        return results
    
    async def unload_all(self) -> Dict[str, bool]:
        """
        Unload all loaded plugins.
        
        Returns:
            Dictionary of plugin_name -> success status
        """
        results = {}
        
        for plugin_name in list(self.registry._plugin_instances.keys()):
            results[plugin_name] = await self.unload_plugin(plugin_name)
        
        return results
    
    async def enable_all(self) -> Dict[str, bool]:
        """
        Enable all loaded plugins.
        
        Returns:
            Dictionary of plugin_name -> success status
        """
        results = {}
        
        for plugin_name in self.registry._plugin_instances.keys():
            results[plugin_name] = await self.enable_plugin(plugin_name)
        
        return results
    
    async def disable_all(self) -> Dict[str, bool]:
        """
        Disable all enabled plugins.
        
        Returns:
            Dictionary of plugin_name -> success status
        """
        results = {}
        
        for plugin_name in self.registry._plugin_instances.keys():
            results[plugin_name] = await self.disable_plugin(plugin_name)
        
        return results
    
    def get_plugin_status(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get status information for a plugin.
        
        Args:
            plugin_name: Name of plugin
            
        Returns:
            Dictionary with plugin status
        """
        registration = self.registry.get_plugin(plugin_name)
        if not registration:
            return None
        
        instance = self.registry.get_plugin_instance(plugin_name)
        
        return {
            "name": registration.metadata.name,
            "version": registration.metadata.version,
            "author": registration.metadata.author,
            "state": instance.state.value if instance else "unloaded",
            "loaded": instance is not None,
            "load_count": registration.load_count,
            "last_error": registration.last_error
        }
    
    def list_loaded_plugins(self) -> List[str]:
        """Get list of currently loaded plugins."""
        return list(self.registry._plugin_instances.keys())
    
    def get_manager_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the plugin manager.
        
        Returns:
            Dictionary with manager statistics
        """
        loaded_plugins = self.list_loaded_plugins()
        enabled_count = sum(
            1 for name in loaded_plugins
            if self.registry.get_plugin_instance(name).state == PluginState.ENABLED
        )
        
        return {
            "total_registered": len(self.registry._registered_plugins),
            "total_loaded": len(loaded_plugins),
            "total_enabled": enabled_count,
            "registry_stats": self.registry.get_registry_stats(),
            "hook_stats": self.hook_manager.get_execution_stats()
        }


# Example usage
async def example_usage():
    """Example of using the plugin manager."""
    from pathlib import Path
    
    # Create manager
    manager = PluginManager(
        plugin_directories=[Path("plugins/examples")]
    )
    
    # Discover plugins
    manager.registry.discover_plugins()
    
    # Load specific plugin
    success = await manager.load_plugin(
        "analytics-plugin",
        config={"api_key": "test-key", "enabled": True}
    )
    print(f"Load success: {success}")
    
    # Enable plugin
    if success:
        await manager.enable_plugin("analytics-plugin")
    
    # Get status
    status = manager.get_plugin_status("analytics-plugin")
    print(f"Plugin status: {status}")
    
    # Get stats
    stats = manager.get_manager_stats()
    print(f"Manager stats: {stats}")
    
    # Cleanup
    await manager.unload_all()


if __name__ == "__main__":
    asyncio.run(example_usage())
