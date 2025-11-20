"""
Base Plugin Classes for Autonomous UI Engine
Phase 6: Innovation - Plugin System

Defines the base plugin interface and lifecycle hooks.
"""

import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import asyncio

logger = logging.getLogger(__name__)


class PluginState(Enum):
    """Plugin lifecycle states."""
    UNLOADED = "unloaded"
    LOADED = "loaded"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"


@dataclass
class PluginMetadata:
    """Metadata about a plugin."""
    name: str
    version: str
    author: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    config_schema: Optional[Dict[str, Any]] = None


@dataclass
class PluginContext:
    """Context passed to plugins."""
    app_instance: Any  # Reference to main application
    config: Dict[str, Any] = field(default_factory=dict)
    shared_data: Dict[str, Any] = field(default_factory=dict)
    logger: Optional[logging.Logger] = None


class BasePlugin(ABC):
    """
    Base class for all plugins.
    
    Plugins must inherit from this class and implement the required methods.
    """
    
    def __init__(self, context: PluginContext):
        """
        Initialize the plugin.
        
        Args:
            context: Plugin execution context
        """
        self.context = context
        self.state = PluginState.UNLOADED
        self.logger = context.logger or logger
        self._metadata: Optional[PluginMetadata] = None
        
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """
        Return plugin metadata.
        
        Returns:
            PluginMetadata with plugin information
        """
        pass
    
    async def on_load(self) -> None:
        """
        Called when plugin is loaded.
        
        Override this method to perform initialization tasks.
        """
        self.logger.info(f"Plugin {self.metadata.name} loaded")
        self.state = PluginState.LOADED
    
    async def on_unload(self) -> None:
        """
        Called when plugin is unloaded.
        
        Override this method to perform cleanup tasks.
        """
        self.logger.info(f"Plugin {self.metadata.name} unloaded")
        self.state = PluginState.UNLOADED
    
    async def on_enable(self) -> None:
        """
        Called when plugin is enabled.
        
        Override this method to start plugin functionality.
        """
        self.logger.info(f"Plugin {self.metadata.name} enabled")
        self.state = PluginState.ENABLED
    
    async def on_disable(self) -> None:
        """
        Called when plugin is disabled.
        
        Override this method to stop plugin functionality.
        """
        self.logger.info(f"Plugin {self.metadata.name} disabled")
        self.state = PluginState.DISABLED
    
    async def on_error(self, error: Exception) -> None:
        """
        Called when plugin encounters an error.
        
        Args:
            error: The error that occurred
        """
        self.logger.error(f"Plugin {self.metadata.name} error: {error}")
        self.state = PluginState.ERROR
    
    async def on_config_change(self, new_config: Dict[str, Any]) -> None:
        """
        Called when plugin configuration changes.
        
        Args:
            new_config: New configuration dictionary
        """
        self.logger.info(f"Plugin {self.metadata.name} config updated")
        self.context.config.update(new_config)
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """
        Main execution method for the plugin.
        
        Override this method to implement plugin functionality.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Plugin execution result
        """
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate plugin configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if configuration is valid
        """
        if not self.metadata.config_schema:
            return True
        
        # Basic validation (in production, use jsonschema)
        required_keys = self.metadata.config_schema.get("required", [])
        for key in required_keys:
            if key not in config:
                self.logger.error(f"Missing required config key: {key}")
                return False
        
        return True
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.context.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.context.config[key] = value
    
    def get_shared_data(self, key: str, default: Any = None) -> Any:
        """
        Get shared data across plugins.
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Shared data value
        """
        return self.context.shared_data.get(key, default)
    
    def set_shared_data(self, key: str, value: Any) -> None:
        """
        Set shared data accessible by other plugins.
        
        Args:
            key: Data key
            value: Data value
        """
        self.context.shared_data[key] = value
    
    def __repr__(self) -> str:
        """String representation of plugin."""
        return f"<Plugin: {self.metadata.name} v{self.metadata.version} [{self.state.value}]>"


class EventPlugin(BasePlugin):
    """
    Base class for event-driven plugins.
    
    Plugins that need to respond to events should inherit from this class.
    """
    
    def __init__(self, context: PluginContext):
        """Initialize event plugin."""
        super().__init__(context)
        self._event_handlers: Dict[str, List[callable]] = {}
    
    def register_event_handler(self, event_name: str, handler: callable) -> None:
        """
        Register an event handler.
        
        Args:
            event_name: Name of the event to handle
            handler: Handler function
        """
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)
        self.logger.debug(f"Registered handler for event: {event_name}")
    
    async def handle_event(self, event_name: str, *args, **kwargs) -> None:
        """
        Handle an event.
        
        Args:
            event_name: Name of the event
            *args: Event arguments
            **kwargs: Event keyword arguments
        """
        if event_name not in self._event_handlers:
            return
        
        self.logger.debug(f"Handling event: {event_name}")
        for handler in self._event_handlers[event_name]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(*args, **kwargs)
                else:
                    handler(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error in event handler for {event_name}: {e}")
    
    async def execute(self, event_name: str, *args, **kwargs) -> Any:
        """
        Execute plugin for an event.
        
        Args:
            event_name: Name of the event
            *args: Event arguments
            **kwargs: Event keyword arguments
        """
        await self.handle_event(event_name, *args, **kwargs)


class ProcessorPlugin(BasePlugin):
    """
    Base class for data processing plugins.
    
    Plugins that transform or process data should inherit from this class.
    """
    
    async def process(self, data: Any, **options) -> Any:
        """
        Process input data.
        
        Args:
            data: Input data to process
            **options: Processing options
            
        Returns:
            Processed data
        """
        return await self.execute(data, **options)
    
    async def execute(self, data: Any, **options) -> Any:
        """
        Execute plugin processing.
        
        Args:
            data: Input data
            **options: Processing options
            
        Returns:
            Processed result
        """
        # Default implementation - return data as-is
        return data


class UIPlugin(BasePlugin):
    """
    Base class for UI-related plugins.
    
    Plugins that enhance or modify UI should inherit from this class.
    """
    
    async def render_component(self, component_type: str, props: Dict[str, Any]) -> str:
        """
        Render a UI component.
        
        Args:
            component_type: Type of component to render
            props: Component properties
            
        Returns:
            Rendered component HTML/code
        """
        return await self.execute(component_type=component_type, props=props)
    
    async def enhance_ui(self, ui_code: str, **options) -> str:
        """
        Enhance existing UI code.
        
        Args:
            ui_code: Original UI code
            **options: Enhancement options
            
        Returns:
            Enhanced UI code
        """
        return await self.execute(ui_code=ui_code, **options)
    
    async def execute(self, **kwargs) -> Any:
        """
        Execute UI plugin functionality.
        
        Args:
            **kwargs: Execution parameters
            
        Returns:
            Result of UI operation
        """
        # Default implementation
        return kwargs.get("ui_code", "")


# Example plugin implementation
class ExamplePlugin(BasePlugin):
    """Example plugin implementation."""
    
    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        return PluginMetadata(
            name="example-plugin",
            version="1.0.0",
            author="Example Author",
            description="An example plugin demonstrating the plugin system",
            tags=["example", "demo"],
            config_schema={
                "required": ["api_key"],
                "properties": {
                    "api_key": {"type": "string"},
                    "enabled": {"type": "boolean", "default": True}
                }
            }
        )
    
    async def on_load(self) -> None:
        """Called when plugin is loaded."""
        await super().on_load()
        self.logger.info("Example plugin loaded successfully")
    
    async def execute(self, *args, **kwargs) -> Any:
        """Execute plugin functionality."""
        return {"status": "success", "message": "Example plugin executed"}


# Example usage
async def example_usage():
    """Example of using base plugin classes."""
    # Create plugin context
    context = PluginContext(
        app_instance=None,
        config={"api_key": "test-key"},
        logger=logger
    )
    
    # Create and use plugin
    plugin = ExamplePlugin(context)
    
    # Load plugin
    await plugin.on_load()
    
    # Enable plugin
    await plugin.on_enable()
    
    # Execute plugin
    result = await plugin.execute()
    print(f"Plugin result: {result}")
    
    # Disable and unload
    await plugin.on_disable()
    await plugin.on_unload()
    
    print(f"Plugin state: {plugin.state}")


if __name__ == "__main__":
    asyncio.run(example_usage())
