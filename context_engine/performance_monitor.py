"""
Performance Monitoring System for Context Engine.

Features:
- Real-time performance metrics
- Operation profiling
- Bottleneck detection
- Resource usage tracking
- Performance alerts
"""

from typing import Dict, Any, List, Optional, Callable
import time
import psutil
import threading
from collections import defaultdict, deque
from datetime import datetime
import functools


class PerformanceMetrics:
    """Tracks performance metrics for operations."""
    
    def __init__(self, name: str):
        self.name = name
        self.call_count = 0
        self.total_time = 0.0
        self.min_time = float('inf')
        self.max_time = 0.0
        self.recent_times = deque(maxlen=100)  # Last 100 calls
        self.errors = 0
    
    def record(self, duration: float, error: bool = False) -> None:
        """Record a single operation."""
        self.call_count += 1
        self.total_time += duration
        self.min_time = min(self.min_time, duration)
        self.max_time = max(self.max_time, duration)
        self.recent_times.append(duration)
        if error:
            self.errors += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for this metric."""
        avg_time = self.total_time / self.call_count if self.call_count > 0 else 0
        
        # Calculate percentiles from recent times
        if self.recent_times:
            sorted_times = sorted(self.recent_times)
            p50 = sorted_times[len(sorted_times) // 2]
            p95 = sorted_times[int(len(sorted_times) * 0.95)]
            p99 = sorted_times[int(len(sorted_times) * 0.99)]
        else:
            p50 = p95 = p99 = 0
        
        return {
            'name': self.name,
            'calls': self.call_count,
            'total_time': self.total_time,
            'avg_time': avg_time,
            'min_time': self.min_time if self.min_time != float('inf') else 0,
            'max_time': self.max_time,
            'p50': p50,
            'p95': p95,
            'p99': p99,
            'errors': self.errors,
            'error_rate': self.errors / self.call_count if self.call_count > 0 else 0
        }


class PerformanceMonitor:
    """
    Real-time performance monitoring system.
    
    Features:
    - Operation profiling
    - Resource tracking (CPU, memory)
    - Bottleneck detection
    - Performance alerts
    - Trend analysis
    """
    
    def __init__(
        self,
        enable_profiling: bool = True,
        enable_resource_tracking: bool = True,
        alert_threshold_ms: float = 1000.0
    ):
        """
        Initialize performance monitor.
        
        Args:
            enable_profiling: Enable operation profiling
            enable_resource_tracking: Enable CPU/memory tracking
            alert_threshold_ms: Alert threshold in milliseconds
        """
        self.enable_profiling = enable_profiling
        self.enable_resource_tracking = enable_resource_tracking
        self.alert_threshold_ms = alert_threshold_ms
        
        # Metrics storage
        self.metrics: Dict[str, PerformanceMetrics] = defaultdict(
            lambda: PerformanceMetrics("")
        )
        
        # Resource tracking
        self.process = psutil.Process()
        self.resource_history = deque(maxlen=1000)
        
        # Alerts
        self.alerts: List[Dict[str, Any]] = []
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Start resource tracking thread
        if enable_resource_tracking:
            self._start_resource_tracking()
    
    def _start_resource_tracking(self) -> None:
        """Start background resource tracking."""
        def track_resources():
            while True:
                try:
                    cpu_percent = self.process.cpu_percent(interval=1)
                    memory_info = self.process.memory_info()
                    
                    self.resource_history.append({
                        'timestamp': time.time(),
                        'cpu_percent': cpu_percent,
                        'memory_mb': memory_info.rss / (1024 * 1024),
                        'memory_percent': self.process.memory_percent()
                    })
                except:
                    pass
                
                time.sleep(5)  # Sample every 5 seconds
        
        thread = threading.Thread(target=track_resources, daemon=True)
        thread.start()
    
    def profile(self, operation_name: str) -> Callable:
        """
        Decorator for profiling operations.
        
        Usage:
            @monitor.profile("my_operation")
            def my_function():
                pass
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enable_profiling:
                    return func(*args, **kwargs)
                
                start_time = time.time()
                error_occurred = False
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    error_occurred = True
                    raise e
                finally:
                    duration = time.time() - start_time
                    
                    with self.lock:
                        if operation_name not in self.metrics:
                            self.metrics[operation_name] = PerformanceMetrics(operation_name)
                        
                        self.metrics[operation_name].record(duration, error_occurred)
                        
                        # Check for performance alert
                        if duration * 1000 > self.alert_threshold_ms:
                            self._add_alert(
                                operation_name,
                                duration,
                                f"Operation exceeded threshold ({self.alert_threshold_ms}ms)"
                            )
            
            return wrapper
        return decorator
    
    def time_operation(self, operation_name: str):
        """
        Context manager for timing operations.
        
        Usage:
            with monitor.time_operation("my_operation"):
                # code to time
                pass
        """
        return OperationTimer(self, operation_name)
    
    def record_operation(
        self,
        operation_name: str,
        duration: float,
        error: bool = False
    ) -> None:
        """
        Manually record an operation.
        
        Args:
            operation_name: Name of the operation
            duration: Duration in seconds
            error: Whether an error occurred
        """
        with self.lock:
            if operation_name not in self.metrics:
                self.metrics[operation_name] = PerformanceMetrics(operation_name)
            
            self.metrics[operation_name].record(duration, error)
            
            # Check for alert
            if duration * 1000 > self.alert_threshold_ms:
                self._add_alert(
                    operation_name,
                    duration,
                    f"Operation exceeded threshold ({self.alert_threshold_ms}ms)"
                )
    
    def _add_alert(
        self,
        operation_name: str,
        duration: float,
        message: str
    ) -> None:
        """Add a performance alert."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation_name,
            'duration_ms': duration * 1000,
            'message': message
        }
        self.alerts.append(alert)
        
        # Keep only last 1000 alerts
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]
    
    def get_operation_stats(self, operation_name: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a specific operation."""
        with self.lock:
            if operation_name in self.metrics:
                return self.metrics[operation_name].get_stats()
            return None
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get all performance statistics."""
        with self.lock:
            stats = {
                'operations': {
                    name: metrics.get_stats()
                    for name, metrics in self.metrics.items()
                },
                'resource_usage': self._get_resource_stats(),
                'alerts': self.alerts[-10:],  # Last 10 alerts
                'bottlenecks': self._detect_bottlenecks()
            }
            return stats
    
    def _get_resource_stats(self) -> Dict[str, Any]:
        """Get resource usage statistics."""
        if not self.resource_history:
            return {}
        
        recent = list(self.resource_history)[-100:]  # Last 100 samples
        
        cpu_values = [r['cpu_percent'] for r in recent]
        mem_values = [r['memory_mb'] for r in recent]
        
        return {
            'cpu_avg': sum(cpu_values) / len(cpu_values),
            'cpu_max': max(cpu_values),
            'memory_avg_mb': sum(mem_values) / len(mem_values),
            'memory_max_mb': max(mem_values),
            'memory_current_mb': recent[-1]['memory_mb'] if recent else 0
        }
    
    def _detect_bottlenecks(self) -> List[Dict[str, Any]]:
        """Detect performance bottlenecks."""
        bottlenecks = []
        
        # Find slowest operations
        operation_stats = [
            (name, metrics.get_stats())
            for name, metrics in self.metrics.items()
        ]
        
        # Sort by average time
        operation_stats.sort(key=lambda x: x[1]['avg_time'], reverse=True)
        
        # Top 5 slowest operations
        for name, stats in operation_stats[:5]:
            if stats['avg_time'] > 0.1:  # More than 100ms average
                bottlenecks.append({
                    'operation': name,
                    'avg_time_ms': stats['avg_time'] * 1000,
                    'calls': stats['calls'],
                    'total_time_s': stats['total_time'],
                    'severity': 'high' if stats['avg_time'] > 1.0 else 'medium'
                })
        
        return bottlenecks
    
    def get_summary(self) -> str:
        """Get a human-readable summary of performance."""
        stats = self.get_all_stats()
        
        summary = ["=== Performance Summary ===\n"]
        
        # Operations
        summary.append(f"Total Operations: {len(stats['operations'])}\n")
        
        if stats['operations']:
            total_calls = sum(op['calls'] for op in stats['operations'].values())
            total_time = sum(op['total_time'] for op in stats['operations'].values())
            summary.append(f"Total Calls: {total_calls}")
            summary.append(f"Total Time: {total_time:.2f}s\n")
        
        # Resource usage
        if stats['resource_usage']:
            res = stats['resource_usage']
            summary.append(f"CPU Usage: {res['cpu_avg']:.1f}% (avg), {res['cpu_max']:.1f}% (max)")
            summary.append(f"Memory: {res['memory_current_mb']:.1f} MB (current), {res['memory_max_mb']:.1f} MB (max)\n")
        
        # Bottlenecks
        if stats['bottlenecks']:
            summary.append("Bottlenecks Detected:")
            for bottleneck in stats['bottlenecks']:
                summary.append(
                    f"  - {bottleneck['operation']}: "
                    f"{bottleneck['avg_time_ms']:.2f}ms avg "
                    f"({bottleneck['calls']} calls) "
                    f"[{bottleneck['severity']}]"
                )
        
        # Recent alerts
        if stats['alerts']:
            summary.append(f"\nRecent Alerts: {len(stats['alerts'])}")
        
        return "\n".join(summary)
    
    def reset(self) -> None:
        """Reset all metrics and alerts."""
        with self.lock:
            self.metrics.clear()
            self.alerts.clear()
            self.resource_history.clear()


class OperationTimer:
    """Context manager for timing operations."""
    
    def __init__(self, monitor: PerformanceMonitor, operation_name: str):
        self.monitor = monitor
        self.operation_name = operation_name
        self.start_time = None
        self.error_occurred = False
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.error_occurred = exc_type is not None
        
        self.monitor.record_operation(
            self.operation_name,
            duration,
            self.error_occurred
        )
        
        return False  # Don't suppress exceptions
