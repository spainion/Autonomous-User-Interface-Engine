"""
Plugin Registry and Discovery for Autonomous UI Engine
Phase 6: Innovation - Plugin System

Handles plugin discovery, registration, and metadata management.
"""

import logging
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Type, Any
from dataclasses import dataclass, field
import asyncio

from .plugin_base import BasePlugin, PluginMetadata, PluginState, PluginContext

logger = logging.getLogger(__name__)


@dataclass
class PluginRegistration:
    """Represents a registered plugin."""
    plugin_class: Type[BasePlugin]
    metadata: PluginMetadata
    instance: Optional[BasePlugin] = None
    file_path: Optional[Path] = None
    load_count: int = 0
    last_error: Optional[str] = None


class PluginRegistry:
    """
    Registry for plugin discovery and management.
    """
    
    def __init__(self, plugin_directories: Optional[List[Path]] = None):
        """
        Initialize the plugin registry.
        
        Args:
            plugin_directories: List of directories to search for plugins
        """
        self.plugin_directories = plugin_directories or []
        self._registered_plugins: Dict[str, PluginRegistration] = {}
        self._plugin_instances: Dict[str, BasePlugin] = {}
        
    def register_plugin(
        self,
        plugin_class: Type[BasePlugin],
        file_path: Optional[Path] = None
    ) -> bool:
        """
        Register a plugin class.
        
        Args:
            plugin_class: Plugin class to register
            file_path: Optional path to plugin file
            
        Returns:
            True if registration successful
        """
        try:
            # Create temporary instance to get metadata
            temp_context = PluginContext(app_instance=None)
            temp_instance = plugin_class(temp_context)
            metadata = temp_instance.metadata
            
            # Check if already registered
            if metadata.name in self._registered_plugins:
                logger.warning(f"Plugin {metadata.name} already registered, updating...")
            
            # Register plugin
            registration = PluginRegistration(
                plugin_class=plugin_class,
                metadata=metadata,
                file_path=file_path
            )
            
            self._registered_plugins[metadata.name] = registration
            logger.info(f"Registered plugin: {metadata.name} v{metadata.version}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to register plugin {plugin_class.__name__}: {e}")
            return False
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        Unregister a plugin.
        
        Args:
            plugin_name: Name of plugin to unregister
            
        Returns:
            True if unregistration successful
        """
        if plugin_name not in self._registered_plugins:
            logger.warning(f"Plugin {plugin_name} not registered")
            return False
        
        # Unload instance if exists
        if plugin_name in self._plugin_instances:
            instance = self._plugin_instances[plugin_name]
            asyncio.create_task(instance.on_unload())
            del self._plugin_instances[plugin_name]
        
        # Remove registration
        del self._registered_plugins[plugin_name]
        logger.info(f"Unregistered plugin: {plugin_name}")
        
        return True
    
    def discover_plugins(self, directory: Optional[Path] = None) -> List[str]:
        """
        Discover plugins in specified or registered directories.
        
        Args:
            directory: Optional specific directory to search
            
        Returns:
            List of discovered plugin names
        """
        directories = [directory] if directory else self.plugin_directories
        discovered = []
        
        for dir_path in directories:
            if not dir_path.exists():
                logger.warning(f"Plugin directory does not exist: {dir_path}")
                continue
            
            logger.info(f"Discovering plugins in: {dir_path}")
            
            # Find Python files
            for file_path in dir_path.glob("*.py"):
                if file_path.name.startswith("_"):
                    continue
                
                try:
                    plugins = self._load_plugins_from_file(file_path)
                    discovered.extend(plugins)
                except Exception as e:
                    logger.error(f"Error loading plugins from {file_path}: {e}")
        
        logger.info(f"Discovered {len(discovered)} plugins")
        return discovered
    
    def _load_plugins_from_file(self, file_path: Path) -> List[str]:
        """
        Load plugins from a Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            List of loaded plugin names
        """
        loaded = []
        
        # Import module
        module_name = file_path.stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            return loaded
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find plugin classes
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, BasePlugin) and 
                obj is not BasePlugin and
                not name.startswith("_")):
                
                if self.register_plugin(obj, file_path):
                    loaded.append(obj.__name__)
        
        return loaded
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginRegistration]:
        """
        Get plugin registration by name.
        
        Args:
            plugin_name: Name of plugin
            
        Returns:
            PluginRegistration or None
        """
        return self._registered_plugins.get(plugin_name)
    
    def list_plugins(
        self,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None
    ) -> List[PluginMetadata]:
        """
        List registered plugins with optional filtering.
        
        Args:
            tags: Optional list of tags to filter by
            author: Optional author name to filter by
            
        Returns:
            List of plugin metadata
        """
        plugins = []
        
        for registration in self._registered_plugins.values():
            metadata = registration.metadata
            
            # Apply filters
            if tags and not any(tag in metadata.tags for tag in tags):
                continue
            
            if author and metadata.author != author:
                continue
            
            plugins.append(metadata)
        
        return plugins
    
    def get_plugin_instance(self, plugin_name: str) -> Optional[BasePlugin]:
        """
        Get loaded plugin instance.
        
        Args:
            plugin_name: Name of plugin
            
        Returns:
            Plugin instance or None
        """
        return self._plugin_instances.get(plugin_name)
    
    def is_plugin_loaded(self, plugin_name: str) -> bool:
        """
        Check if plugin is loaded.
        
        Args:
            plugin_name: Name of plugin
            
        Returns:
            True if plugin is loaded
        """
        return plugin_name in self._plugin_instances
    
    def get_dependencies(self, plugin_name: str) -> List[str]:
        """
        Get dependencies for a plugin.
        
        Args:
            plugin_name: Name of plugin
            
        Returns:
            List of dependency names
        """
        registration = self._registered_plugins.get(plugin_name)
        if not registration:
            return []
        
        return registration.metadata.dependencies
    
    def check_dependencies(self, plugin_name: str) -> Tuple[bool, List[str]]:
        """
        Check if all dependencies for a plugin are satisfied.
        
        Args:
            plugin_name: Name of plugin
            
        Returns:
            Tuple of (all_satisfied, missing_dependencies)
        """
        dependencies = self.get_dependencies(plugin_name)
        missing = []
        
        for dep in dependencies:
            if dep not in self._registered_plugins:
                missing.append(dep)
        
        return len(missing) == 0, missing
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the plugin registry.
        
        Returns:
            Dictionary with registry statistics
        """
        total_registered = len(self._registered_plugins)
        total_loaded = len(self._plugin_instances)
        
        # Count by tags
        tag_counts = {}
        for registration in self._registered_plugins.values():
            for tag in registration.metadata.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Count by author
        author_counts = {}
        for registration in self._registered_plugins.values():
            author = registration.metadata.author
            author_counts[author] = author_counts.get(author, 0) + 1
        
        return {
            "total_registered": total_registered,
            "total_loaded": total_loaded,
            "tag_distribution": tag_counts,
            "author_distribution": author_counts
        }
    
    def search_plugins(self, query: str) -> List[PluginMetadata]:
        """
        Search plugins by name, description, or tags.
        
        Args:
            query: Search query
            
        Returns:
            List of matching plugin metadata
        """
        query_lower = query.lower()
        matches = []
        
        for registration in self._registered_plugins.values():
            metadata = registration.metadata
            
            # Search in name, description, and tags
            if (query_lower in metadata.name.lower() or
                query_lower in metadata.description.lower() or
                any(query_lower in tag.lower() for tag in metadata.tags)):
                matches.append(metadata)
        
        return matches
    
    def export_registry(self) -> Dict[str, Any]:
        """
        Export registry data for serialization.
        
        Returns:
            Dictionary with registry data
        """
        plugins_data = []
        
        for name, registration in self._registered_plugins.items():
            metadata = registration.metadata
            plugins_data.append({
                "name": metadata.name,
                "version": metadata.version,
                "author": metadata.author,
                "description": metadata.description,
                "tags": metadata.tags,
                "dependencies": metadata.dependencies,
                "file_path": str(registration.file_path) if registration.file_path else None,
                "load_count": registration.load_count
            })
        
        return {
            "plugins": plugins_data,
            "stats": self.get_registry_stats()
        }


# Global registry instance
_plugin_registry = PluginRegistry()


def get_plugin_registry() -> PluginRegistry:
    """Get the global plugin registry instance."""
    return _plugin_registry


def register_plugin(plugin_class: Type[BasePlugin], file_path: Optional[Path] = None) -> bool:
    """Register a plugin in the global registry."""
    return _plugin_registry.register_plugin(plugin_class, file_path)


def discover_plugins(directory: Optional[Path] = None) -> List[str]:
    """Discover plugins using the global registry."""
    return _plugin_registry.discover_plugins(directory)


def list_plugins(tags: Optional[List[str]] = None, author: Optional[str] = None) -> List[PluginMetadata]:
    """List plugins using the global registry."""
    return _plugin_registry.list_plugins(tags, author)


def search_plugins(query: str) -> List[PluginMetadata]:
    """Search plugins using the global registry."""
    return _plugin_registry.search_plugins(query)


# Example usage
def example_usage():
    """Example of using the plugin registry."""
    from pathlib import Path
    
    # Create registry
    registry = PluginRegistry(plugin_directories=[Path("plugins/examples")])
    
    # Discover plugins
    discovered = registry.discover_plugins()
    print(f"Discovered plugins: {discovered}")
    
    # List all plugins
    all_plugins = registry.list_plugins()
    for metadata in all_plugins:
        print(f"- {metadata.name} v{metadata.version} by {metadata.author}")
    
    # Search plugins
    results = registry.search_plugins("analytics")
    print(f"\nSearch results for 'analytics': {len(results)}")
    
    # Get stats
    stats = registry.get_registry_stats()
    print(f"\nRegistry Stats: {stats}")


if __name__ == "__main__":
    example_usage()
