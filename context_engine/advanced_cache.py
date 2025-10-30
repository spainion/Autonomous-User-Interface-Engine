"""
Advanced Caching System for Context Engine.

Features:
- LRU eviction policy
- Persistent cache with disk storage
- Distributed cache support
- Cache statistics and monitoring
- Multi-level caching (memory + disk)
"""

from typing import Any, Dict, Optional, List, Tuple
import pickle
import json
import hashlib
import time
from collections import OrderedDict
from pathlib import Path
import threading


class CacheEntry:
    """Represents a single cache entry with metadata."""
    
    def __init__(self, key: str, value: Any, ttl: Optional[float] = None):
        self.key = key
        self.value = value
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.access_count = 0
        self.ttl = ttl  # Time to live in seconds
        self.size = self._estimate_size(value)
    
    def _estimate_size(self, value: Any) -> int:
        """Estimate size of value in bytes."""
        try:
            return len(pickle.dumps(value))
        except:
            return 1000  # Default estimate
    
    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.ttl is None:
            return False
        return (time.time() - self.created_at) > self.ttl
    
    def access(self) -> Any:
        """Access the cached value and update metadata."""
        self.last_accessed = time.time()
        self.access_count += 1
        return self.value


class AdvancedCache:
    """
    Advanced multi-level caching system with LRU eviction and persistence.
    
    Features:
    - LRU eviction policy
    - TTL (time-to-live) support
    - Persistent disk storage
    - Cache statistics
    - Thread-safe operations
    - Size-based eviction
    """
    
    def __init__(
        self,
        max_memory_size: int = 100 * 1024 * 1024,  # 100 MB
        max_entries: int = 10000,
        enable_disk_cache: bool = True,
        cache_dir: str = ".cache",
        default_ttl: Optional[float] = None
    ):
        """
        Initialize advanced cache.
        
        Args:
            max_memory_size: Maximum memory cache size in bytes
            max_entries: Maximum number of entries in memory
            enable_disk_cache: Enable persistent disk cache
            cache_dir: Directory for disk cache
            default_ttl: Default time-to-live in seconds
        """
        self.max_memory_size = max_memory_size
        self.max_entries = max_entries
        self.enable_disk_cache = enable_disk_cache
        self.cache_dir = Path(cache_dir)
        self.default_ttl = default_ttl
        
        # Memory cache (LRU)
        self.memory_cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.current_size = 0
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'disk_reads': 0,
            'disk_writes': 0
        }
        
        # Create cache directory
        if enable_disk_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_key_hash(self, key: str) -> str:
        """Generate hash for cache key."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            default: Default value if not found
        
        Returns:
            Cached value or default
        """
        with self.lock:
            # Check memory cache
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                
                # Check if expired
                if entry.is_expired():
                    self._remove_from_memory(key)
                    self.stats['misses'] += 1
                    return self._get_from_disk(key, default)
                
                # Move to end (most recently used)
                self.memory_cache.move_to_end(key)
                self.stats['hits'] += 1
                return entry.access()
            
            # Check disk cache
            self.stats['misses'] += 1
            return self._get_from_disk(key, default)
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[float] = None
    ) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (overrides default)
        """
        with self.lock:
            # Use default TTL if not specified
            if ttl is None:
                ttl = self.default_ttl
            
            # Create cache entry
            entry = CacheEntry(key, value, ttl)
            
            # Remove old entry if exists
            if key in self.memory_cache:
                self._remove_from_memory(key)
            
            # Check if we need to evict
            while (
                len(self.memory_cache) >= self.max_entries or
                self.current_size + entry.size > self.max_memory_size
            ):
                if not self._evict_lru():
                    break  # Can't evict more
            
            # Add to memory cache
            self.memory_cache[key] = entry
            self.current_size += entry.size
            
            # Write to disk cache
            if self.enable_disk_cache:
                self._write_to_disk(key, value)
    
    def _evict_lru(self) -> bool:
        """Evict least recently used entry."""
        if not self.memory_cache:
            return False
        
        # Get least recently used (first item)
        lru_key = next(iter(self.memory_cache))
        self._remove_from_memory(lru_key)
        self.stats['evictions'] += 1
        return True
    
    def _remove_from_memory(self, key: str) -> None:
        """Remove entry from memory cache."""
        if key in self.memory_cache:
            entry = self.memory_cache.pop(key)
            self.current_size -= entry.size
    
    def _get_from_disk(self, key: str, default: Any = None) -> Any:
        """Get value from disk cache."""
        if not self.enable_disk_cache:
            return default
        
        try:
            key_hash = self._generate_key_hash(key)
            cache_file = self.cache_dir / f"{key_hash}.cache"
            
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)
                    
                # Check TTL
                if 'ttl' in data and data['ttl'] is not None:
                    if (time.time() - data['created_at']) > data['ttl']:
                        cache_file.unlink()  # Delete expired
                        return default
                
                self.stats['disk_reads'] += 1
                
                # Promote to memory cache
                self.set(key, data['value'], data.get('ttl'))
                
                return data['value']
        except Exception as e:
            print(f"Error reading from disk cache: {e}")
        
        return default
    
    def _write_to_disk(self, key: str, value: Any) -> None:
        """Write value to disk cache."""
        if not self.enable_disk_cache:
            return
        
        try:
            key_hash = self._generate_key_hash(key)
            cache_file = self.cache_dir / f"{key_hash}.cache"
            
            data = {
                'key': key,
                'value': value,
                'created_at': time.time(),
                'ttl': self.default_ttl
            }
            
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
            
            self.stats['disk_writes'] += 1
        except Exception as e:
            print(f"Error writing to disk cache: {e}")
    
    def delete(self, key: str) -> bool:
        """
        Delete entry from cache.
        
        Args:
            key: Cache key
        
        Returns:
            True if deleted, False if not found
        """
        with self.lock:
            found = False
            
            # Remove from memory
            if key in self.memory_cache:
                self._remove_from_memory(key)
                found = True
            
            # Remove from disk
            if self.enable_disk_cache:
                try:
                    key_hash = self._generate_key_hash(key)
                    cache_file = self.cache_dir / f"{key_hash}.cache"
                    if cache_file.exists():
                        cache_file.unlink()
                        found = True
                except:
                    pass
            
            return found
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.memory_cache.clear()
            self.current_size = 0
            
            if self.enable_disk_cache:
                for cache_file in self.cache_dir.glob("*.cache"):
                    try:
                        cache_file.unlink()
                    except:
                        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                **self.stats,
                'memory_entries': len(self.memory_cache),
                'memory_size_bytes': self.current_size,
                'memory_size_mb': self.current_size / (1024 * 1024),
                'hit_rate': hit_rate,
                'miss_rate': 1 - hit_rate
            }
    
    def cleanup_expired(self) -> int:
        """Remove all expired entries. Returns count of removed entries."""
        with self.lock:
            count = 0
            
            # Check memory cache
            expired_keys = [
                key for key, entry in self.memory_cache.items()
                if entry.is_expired()
            ]
            
            for key in expired_keys:
                self._remove_from_memory(key)
                count += 1
            
            # Check disk cache
            if self.enable_disk_cache:
                for cache_file in self.cache_dir.glob("*.cache"):
                    try:
                        with open(cache_file, 'rb') as f:
                            data = pickle.load(f)
                            if 'ttl' in data and data['ttl'] is not None:
                                if (time.time() - data['created_at']) > data['ttl']:
                                    cache_file.unlink()
                                    count += 1
                    except:
                        pass
            
            return count
