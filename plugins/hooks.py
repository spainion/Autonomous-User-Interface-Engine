"""
Event Hook System for Autonomous UI Engine
Phase 6: Innovation - Plugin System

Provides a decorator-based event hook system for plugins.
"""

import logging
import asyncio
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from functools import wraps
from enum import Enum

logger = logging.getLogger(__name__)


class HookPriority(Enum):
    """Hook execution priority."""
    HIGHEST = 0
    HIGH = 10
    NORMAL = 50
    LOW = 100
    LOWEST = 200


@dataclass
class Hook:
    """Represents a hook registration."""
    event_name: str
    callback: Callable
    priority: HookPriority = HookPriority.NORMAL
    async_callback: bool = False
    plugin_name: Optional[str] = None


@dataclass
class HookResult:
    """Result from hook execution."""
    success: bool
    data: Any = None
    errors: List[Exception] = field(default_factory=list)
    hook_count: int = 0


class HookManager:
    """
    Manages event hooks and provides decorator support.
    """
    
    def __init__(self):
        """Initialize the hook manager."""
        self._hooks: Dict[str, List[Hook]] = {}
        self._execution_history: List[Dict[str, Any]] = []
        
    def register(
        self,
        event_name: str,
        callback: Callable,
        priority: HookPriority = HookPriority.NORMAL,
        plugin_name: Optional[str] = None
    ) -> None:
        """
        Register a hook for an event.
        
        Args:
            event_name: Name of the event to hook into
            callback: Function to call when event is triggered
            priority: Execution priority
            plugin_name: Optional name of plugin registering the hook
        """
        hook = Hook(
            event_name=event_name,
            callback=callback,
            priority=priority,
            async_callback=asyncio.iscoroutinefunction(callback),
            plugin_name=plugin_name
        )
        
        if event_name not in self._hooks:
            self._hooks[event_name] = []
        
        self._hooks[event_name].append(hook)
        
        # Sort by priority
        self._hooks[event_name].sort(key=lambda h: h.priority.value)
        
        logger.debug(
            f"Registered hook for '{event_name}' "
            f"(priority: {priority.value}, plugin: {plugin_name})"
        )
    
    def unregister(
        self,
        event_name: str,
        callback: Optional[Callable] = None,
        plugin_name: Optional[str] = None
    ) -> int:
        """
        Unregister hooks for an event.
        
        Args:
            event_name: Name of the event
            callback: Optional specific callback to remove
            plugin_name: Optional plugin name to remove all hooks for
            
        Returns:
            Number of hooks removed
        """
        if event_name not in self._hooks:
            return 0
        
        original_count = len(self._hooks[event_name])
        
        # Filter hooks based on criteria
        self._hooks[event_name] = [
            hook for hook in self._hooks[event_name]
            if not (
                (callback is None or hook.callback == callback) and
                (plugin_name is None or hook.plugin_name == plugin_name)
            )
        ]
        
        removed_count = original_count - len(self._hooks[event_name])
        
        if removed_count > 0:
            logger.debug(f"Unregistered {removed_count} hooks for '{event_name}'")
        
        return removed_count
    
    async def trigger(
        self,
        event_name: str,
        *args,
        **kwargs
    ) -> HookResult:
        """
        Trigger an event and execute all registered hooks.
        
        Args:
            event_name: Name of the event to trigger
            *args: Positional arguments passed to hooks
            **kwargs: Keyword arguments passed to hooks
            
        Returns:
            HookResult with execution details
        """
        if event_name not in self._hooks:
            return HookResult(success=True, hook_count=0)
        
        logger.debug(f"Triggering event: {event_name}")
        
        errors = []
        results = []
        
        for hook in self._hooks[event_name]:
            try:
                if hook.async_callback:
                    result = await hook.callback(*args, **kwargs)
                else:
                    result = hook.callback(*args, **kwargs)
                
                results.append(result)
                
            except Exception as e:
                logger.error(
                    f"Error executing hook for '{event_name}' "
                    f"(plugin: {hook.plugin_name}): {e}"
                )
                errors.append(e)
        
        # Log execution
        self._execution_history.append({
            "event_name": event_name,
            "hook_count": len(self._hooks[event_name]),
            "errors": len(errors),
            "success": len(errors) == 0
        })
        
        return HookResult(
            success=len(errors) == 0,
            data=results,
            errors=errors,
            hook_count=len(self._hooks[event_name])
        )
    
    def list_hooks(self, event_name: Optional[str] = None) -> Dict[str, List[Hook]]:
        """
        List registered hooks.
        
        Args:
            event_name: Optional event name to filter by
            
        Returns:
            Dictionary of hooks by event name
        """
        if event_name:
            return {event_name: self._hooks.get(event_name, [])}
        return self._hooks.copy()
    
    def get_hook_count(self, event_name: Optional[str] = None) -> int:
        """
        Get count of registered hooks.
        
        Args:
            event_name: Optional event name to count hooks for
            
        Returns:
            Number of hooks
        """
        if event_name:
            return len(self._hooks.get(event_name, []))
        return sum(len(hooks) for hooks in self._hooks.values())
    
    def clear_hooks(self, event_name: Optional[str] = None) -> None:
        """
        Clear hooks for an event or all events.
        
        Args:
            event_name: Optional event name to clear hooks for
        """
        if event_name:
            if event_name in self._hooks:
                del self._hooks[event_name]
                logger.info(f"Cleared hooks for event: {event_name}")
        else:
            self._hooks.clear()
            logger.info("Cleared all hooks")
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """
        Get statistics about hook executions.
        
        Returns:
            Dictionary with execution statistics
        """
        if not self._execution_history:
            return {"total_executions": 0}
        
        total_executions = len(self._execution_history)
        total_errors = sum(e["errors"] for e in self._execution_history)
        successful_executions = sum(1 for e in self._execution_history if e["success"])
        
        event_counts = {}
        for execution in self._execution_history:
            event = execution["event_name"]
            event_counts[event] = event_counts.get(event, 0) + 1
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "total_errors": total_errors,
            "event_distribution": event_counts,
            "registered_events": len(self._hooks),
            "total_hooks": self.get_hook_count()
        }


# Global hook manager instance
_hook_manager = HookManager()


# Decorator functions
def hook(
    event_name: str,
    priority: HookPriority = HookPriority.NORMAL,
    plugin_name: Optional[str] = None
):
    """
    Decorator to register a function as a hook.
    
    Args:
        event_name: Name of the event to hook into
        priority: Execution priority
        plugin_name: Optional plugin name
        
    Example:
        @hook("ui.generate", priority=HookPriority.HIGH)
        async def enhance_ui(ui_code):
            return enhance(ui_code)
    """
    def decorator(func: Callable) -> Callable:
        _hook_manager.register(
            event_name=event_name,
            callback=func,
            priority=priority,
            plugin_name=plugin_name
        )
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator


def before(event_name: str, priority: HookPriority = HookPriority.HIGH):
    """
    Decorator to register a function to run before an event.
    
    Args:
        event_name: Name of the event
        priority: Execution priority (defaults to HIGH)
        
    Example:
        @before("ui.generate")
        async def validate_input(data):
            if not data:
                raise ValueError("No input data")
    """
    return hook(f"before_{event_name}", priority=priority)


def after(event_name: str, priority: HookPriority = HookPriority.LOW):
    """
    Decorator to register a function to run after an event.
    
    Args:
        event_name: Name of the event
        priority: Execution priority (defaults to LOW)
        
    Example:
        @after("ui.generate")
        async def log_result(result):
            logger.info(f"Generated UI: {result}")
    """
    return hook(f"after_{event_name}", priority=priority)


def on_error(event_name: str):
    """
    Decorator to register an error handler for an event.
    
    Args:
        event_name: Name of the event
        
    Example:
        @on_error("ui.generate")
        async def handle_error(error):
            logger.error(f"UI generation failed: {error}")
    """
    return hook(f"error_{event_name}", priority=HookPriority.HIGHEST)


# Convenience functions
def register_hook(
    event_name: str,
    callback: Callable,
    priority: HookPriority = HookPriority.NORMAL,
    plugin_name: Optional[str] = None
) -> None:
    """Register a hook programmatically."""
    _hook_manager.register(event_name, callback, priority, plugin_name)


def unregister_hook(
    event_name: str,
    callback: Optional[Callable] = None,
    plugin_name: Optional[str] = None
) -> int:
    """Unregister hooks programmatically."""
    return _hook_manager.unregister(event_name, callback, plugin_name)


async def trigger_hook(event_name: str, *args, **kwargs) -> HookResult:
    """Trigger an event programmatically."""
    return await _hook_manager.trigger(event_name, *args, **kwargs)


def get_hook_manager() -> HookManager:
    """Get the global hook manager instance."""
    return _hook_manager


# Predefined event names
class Events:
    """Standard event names used by the system."""
    
    # UI Generation events
    UI_GENERATE_START = "ui.generate.start"
    UI_GENERATE_COMPLETE = "ui.generate.complete"
    UI_GENERATE_ERROR = "ui.generate.error"
    
    # Agent events
    AGENT_START = "agent.start"
    AGENT_COMPLETE = "agent.complete"
    AGENT_ERROR = "agent.error"
    
    # Context events
    CONTEXT_ADD = "context.add"
    CONTEXT_RETRIEVE = "context.retrieve"
    CONTEXT_UPDATE = "context.update"
    
    # Plugin events
    PLUGIN_LOAD = "plugin.load"
    PLUGIN_UNLOAD = "plugin.unload"
    PLUGIN_ENABLE = "plugin.enable"
    PLUGIN_DISABLE = "plugin.disable"
    PLUGIN_ERROR = "plugin.error"
    
    # System events
    SYSTEM_START = "system.start"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_ERROR = "system.error"


# Example usage
async def example_usage():
    """Example of using the hook system."""
    
    # Using decorators
    @hook(Events.UI_GENERATE_START, priority=HookPriority.HIGH)
    async def validate_ui_input(ui_type: str):
        print(f"Validating UI input: {ui_type}")
        return {"validated": True}
    
    @hook(Events.UI_GENERATE_COMPLETE, priority=HookPriority.NORMAL)
    async def log_ui_generation(result: str):
        print(f"UI generated: {result[:50]}...")
    
    @hook(Events.UI_GENERATE_COMPLETE, priority=HookPriority.LOW)
    async def notify_completion():
        print("Sending completion notification")
    
    # Trigger events
    result1 = await trigger_hook(Events.UI_GENERATE_START, "dashboard")
    print(f"Start hooks result: {result1.success}, count: {result1.hook_count}")
    
    result2 = await trigger_hook(Events.UI_GENERATE_COMPLETE, "<div>Dashboard</div>")
    print(f"Complete hooks result: {result2.success}, count: {result2.hook_count}")
    
    # Get stats
    stats = _hook_manager.get_execution_stats()
    print(f"\nHook Stats: {stats}")


if __name__ == "__main__":
    asyncio.run(example_usage())
