"""
Notification Plugin Example for Autonomous UI Engine
Phase 6: Innovation - Plugin System
"""

from typing import Dict, Any, List
from datetime import datetime
from plugins.plugin_base import EventPlugin, PluginMetadata

class NotificationPlugin(EventPlugin):
    """Example plugin that handles notifications."""
    
    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        return PluginMetadata(
            name="notification-plugin",
            version="1.0.0",
            author="UI Engine Team",
            description="Handles notifications and alerts",
            tags=["notification", "alerts", "messaging"],
            config_schema={
                "properties": {
                    "channels": {"type": "array", "default": ["console"]},
                    "level": {"type": "string", "default": "info"}
                }
            }
        )
    
    async def on_load(self) -> None:
        """Initialize notification system."""
        await super().on_load()
        self._notifications: List[Dict[str, Any]] = []
        self._channels = self.get_config("channels", ["console"])
    
    async def execute(self, *args, **kwargs) -> Any:
        """Send a notification."""
        message = kwargs.get("message", "")
        level = kwargs.get("level", "info")
        channel = kwargs.get("channel", "console")
        
        notification = {
            "message": message,
            "level": level,
            "channel": channel,
            "timestamp": datetime.now().isoformat()
        }
        
        self._notifications.append(notification)
        
        # Send to channel
        if channel == "console":
            self.logger.info(f"[{level.upper()}] {message}")
        
        return {"success": True, "notification": notification}
    
    def get_recent_notifications(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent notifications."""
        return self._notifications[-limit:]
