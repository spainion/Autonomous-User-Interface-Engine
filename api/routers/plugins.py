"""
Plugin Management Router for Autonomous UI Engine API
Phase 6: Innovation - API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path

from plugins.plugin_manager import PluginManager
from plugins.registry import get_plugin_registry

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize plugin manager
plugin_manager = PluginManager(
    plugin_directories=[Path("plugins/examples")]
)


# Request/Response models
class PluginLoadRequest(BaseModel):
    """Request to load a plugin."""
    plugin_name: str = Field(..., description="Name of plugin to load")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)


class PluginExecuteRequest(BaseModel):
    """Request to execute a plugin."""
    plugin_name: str = Field(..., description="Name of plugin to execute")
    args: Optional[List[Any]] = Field(default_factory=list)
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict)


@router.post("/load")
async def load_plugin(request: PluginLoadRequest):
    """Load a plugin."""
    try:
        success = await plugin_manager.load_plugin(
            request.plugin_name,
            request.config
        )
        
        if success:
            status = plugin_manager.get_plugin_status(request.plugin_name)
            return {
                "success": True,
                "message": f"Plugin {request.plugin_name} loaded successfully",
                "status": status
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to load plugin {request.plugin_name}"
            )
    except Exception as e:
        logger.error(f"Error loading plugin: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/unload/{plugin_name}")
async def unload_plugin(plugin_name: str):
    """Unload a plugin."""
    try:
        success = await plugin_manager.unload_plugin(plugin_name)
        
        if success:
            return {
                "success": True,
                "message": f"Plugin {plugin_name} unloaded successfully"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Plugin {plugin_name} not loaded"
            )
    except Exception as e:
        logger.error(f"Error unloading plugin: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enable/{plugin_name}")
async def enable_plugin(plugin_name: str):
    """Enable a loaded plugin."""
    try:
        success = await plugin_manager.enable_plugin(plugin_name)
        
        if success:
            return {
                "success": True,
                "message": f"Plugin {plugin_name} enabled successfully"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to enable plugin {plugin_name}"
            )
    except Exception as e:
        logger.error(f"Error enabling plugin: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/disable/{plugin_name}")
async def disable_plugin(plugin_name: str):
    """Disable an enabled plugin."""
    try:
        success = await plugin_manager.disable_plugin(plugin_name)
        
        if success:
            return {
                "success": True,
                "message": f"Plugin {plugin_name} disabled successfully"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to disable plugin {plugin_name}"
            )
    except Exception as e:
        logger.error(f"Error disabling plugin: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reload/{plugin_name}")
async def reload_plugin(plugin_name: str):
    """Reload a plugin."""
    try:
        success = await plugin_manager.reload_plugin(plugin_name)
        
        if success:
            return {
                "success": True,
                "message": f"Plugin {plugin_name} reloaded successfully"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to reload plugin {plugin_name}"
            )
    except Exception as e:
        logger.error(f"Error reloading plugin: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute_plugin(request: PluginExecuteRequest):
    """Execute a plugin."""
    try:
        result = await plugin_manager.execute_plugin(
            request.plugin_name,
            *request.args,
            **request.kwargs
        )
        
        return {
            "success": True,
            "plugin": request.plugin_name,
            "result": result
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing plugin: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_plugins(
    tags: Optional[str] = None,
    author: Optional[str] = None
):
    """List all available plugins."""
    try:
        registry = get_plugin_registry()
        
        # Parse tags
        tag_list = tags.split(",") if tags else None
        
        plugins = registry.list_plugins(tags=tag_list, author=author)
        
        return {
            "success": True,
            "count": len(plugins),
            "plugins": [
                {
                    "name": p.name,
                    "version": p.version,
                    "author": p.author,
                    "description": p.description,
                    "tags": p.tags
                }
                for p in plugins
            ]
        }
    except Exception as e:
        logger.error(f"Error listing plugins: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/loaded")
async def list_loaded_plugins():
    """List currently loaded plugins."""
    try:
        loaded = plugin_manager.list_loaded_plugins()
        
        statuses = []
        for plugin_name in loaded:
            status = plugin_manager.get_plugin_status(plugin_name)
            if status:
                statuses.append(status)
        
        return {
            "success": True,
            "count": len(statuses),
            "plugins": statuses
        }
    except Exception as e:
        logger.error(f"Error listing loaded plugins: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{plugin_name}")
async def get_plugin_status(plugin_name: str):
    """Get status of a specific plugin."""
    try:
        status = plugin_manager.get_plugin_status(plugin_name)
        
        if status:
            return {"success": True, "status": status}
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Plugin {plugin_name} not found"
            )
    except Exception as e:
        logger.error(f"Error getting plugin status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_plugins(q: str):
    """Search for plugins."""
    try:
        registry = get_plugin_registry()
        results = registry.search_plugins(q)
        
        return {
            "success": True,
            "query": q,
            "count": len(results),
            "results": [
                {
                    "name": p.name,
                    "version": p.version,
                    "description": p.description,
                    "tags": p.tags
                }
                for p in results
            ]
        }
    except Exception as e:
        logger.error(f"Error searching plugins: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discover")
async def discover_plugins():
    """Discover plugins in registered directories."""
    try:
        discovered = plugin_manager.registry.discover_plugins()
        
        return {
            "success": True,
            "count": len(discovered),
            "plugins": discovered
        }
    except Exception as e:
        logger.error(f"Error discovering plugins: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_plugin_stats():
    """Get plugin manager statistics."""
    try:
        stats = plugin_manager.get_manager_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Error getting plugin stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def plugin_health_check():
    """Check health of plugin system."""
    return {
        "status": "healthy",
        "plugin_system": "available",
        "total_registered": len(plugin_manager.registry._registered_plugins),
        "total_loaded": len(plugin_manager.list_loaded_plugins())
    }
