"""
Configuration Management System

Centralized configuration management for all system components with
environment-specific settings, validation, and hot-reloading.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from enum import Enum
import copy


class Environment(Enum):
    """Deployment environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    database: str = "autonomous_ui"
    username: str = "admin"
    password: str = ""
    pool_size: int = 10
    pool_timeout: int = 30
    ssl_enabled: bool = False


@dataclass
class LLMConfig:
    """LLM orchestrator configuration"""
    api_key: str = ""
    default_model: str = "gpt-4-turbo"
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 30
    retry_attempts: int = 3
    cache_enabled: bool = True
    cache_ttl: int = 3600
    cost_limit_per_day: float = 100.0


@dataclass
class NLPConfig:
    """NLP system configuration"""
    default_language: str = "en"
    confidence_threshold: float = 0.7
    max_entities: int = 50
    sentiment_enabled: bool = True
    language_detection_enabled: bool = True


@dataclass
class UIBuilderConfig:
    """UI builder configuration"""
    default_framework: str = "react"
    enable_accessibility: bool = True
    enable_responsive: bool = True
    enable_pwa: bool = False
    default_theme: str = "light"
    component_cache_enabled: bool = True


@dataclass
class APIConfig:
    """API configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    cors_enabled: bool = True
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    auth_enabled: bool = False
    auth_type: str = "bearer"


@dataclass
class AgentConfig:
    """Multi-agent system configuration"""
    max_workers: int = 10
    coordination_strategy: str = "parallel"
    task_timeout: int = 300
    quality_threshold: float = 0.8
    enable_learning: bool = True


@dataclass
class ExecutorConfig:
    """Autonomous executor configuration"""
    changes_per_round: int = 10
    max_iterations: int = 5
    min_quality_score: float = 0.7
    parallel_execution: bool = True
    adaptive_strategy: bool = True


@dataclass
class MonitoringConfig:
    """Monitoring and observability configuration"""
    enabled: bool = True
    log_level: str = "INFO"
    metrics_enabled: bool = True
    tracing_enabled: bool = False
    health_check_interval: int = 60


@dataclass
class SystemConfig:
    """Complete system configuration"""
    environment: str = "development"
    debug: bool = False
    
    # Component configs
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    nlp: NLPConfig = field(default_factory=NLPConfig)
    ui_builder: UIBuilderConfig = field(default_factory=UIBuilderConfig)
    api: APIConfig = field(default_factory=APIConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    executor: ExecutorConfig = field(default_factory=ExecutorConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)


class ConfigManager:
    """Configuration management system"""
    
    def __init__(self, environment: str = None):
        """
        Initialize configuration manager.
        
        Args:
            environment: Deployment environment (development, staging, production)
        """
        self.environment = environment or os.getenv('ENVIRONMENT', 'development')
        self.config = SystemConfig(environment=self.environment)
        self._config_file = None
        self._loaded = False
    
    def load_from_file(self, config_path: str) -> 'ConfigManager':
        """
        Load configuration from file (JSON or YAML).
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Self for method chaining
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            if config_path.endswith('.json'):
                data = json.load(f)
            elif config_path.endswith(('.yml', '.yaml')):
                data = yaml.safe_load(f)
            else:
                raise ValueError("Config file must be JSON or YAML")
        
        self._apply_config_data(data)
        self._config_file = config_path
        self._loaded = True
        
        return self
    
    def load_from_env(self) -> 'ConfigManager':
        """
        Load configuration from environment variables.
        
        Returns:
            Self for method chaining
        """
        # Database
        if os.getenv('DB_HOST'):
            self.config.database.host = os.getenv('DB_HOST')
        if os.getenv('DB_PORT'):
            self.config.database.port = int(os.getenv('DB_PORT'))
        if os.getenv('DB_NAME'):
            self.config.database.database = os.getenv('DB_NAME')
        if os.getenv('DB_USER'):
            self.config.database.username = os.getenv('DB_USER')
        if os.getenv('DB_PASSWORD'):
            self.config.database.password = os.getenv('DB_PASSWORD')
        
        # LLM
        if os.getenv('OPENROUTER_API_KEY'):
            self.config.llm.api_key = os.getenv('OPENROUTER_API_KEY')
        if os.getenv('LLM_DEFAULT_MODEL'):
            self.config.llm.default_model = os.getenv('LLM_DEFAULT_MODEL')
        if os.getenv('LLM_MAX_TOKENS'):
            self.config.llm.max_tokens = int(os.getenv('LLM_MAX_TOKENS'))
        
        # API
        if os.getenv('API_HOST'):
            self.config.api.host = os.getenv('API_HOST')
        if os.getenv('API_PORT'):
            self.config.api.port = int(os.getenv('API_PORT'))
        
        # Debug
        if os.getenv('DEBUG'):
            self.config.debug = os.getenv('DEBUG').lower() in ('true', '1', 'yes')
        
        self._loaded = True
        return self
    
    def _apply_config_data(self, data: Dict[str, Any]):
        """Apply configuration data to config object"""
        if 'environment' in data:
            self.config.environment = data['environment']
        if 'debug' in data:
            self.config.debug = data['debug']
        
        # Apply component configs
        if 'database' in data:
            for key, value in data['database'].items():
                if hasattr(self.config.database, key):
                    setattr(self.config.database, key, value)
        
        if 'llm' in data:
            for key, value in data['llm'].items():
                if hasattr(self.config.llm, key):
                    setattr(self.config.llm, key, value)
        
        if 'nlp' in data:
            for key, value in data['nlp'].items():
                if hasattr(self.config.nlp, key):
                    setattr(self.config.nlp, key, value)
        
        if 'ui_builder' in data:
            for key, value in data['ui_builder'].items():
                if hasattr(self.config.ui_builder, key):
                    setattr(self.config.ui_builder, key, value)
        
        if 'api' in data:
            for key, value in data['api'].items():
                if hasattr(self.config.api, key):
                    setattr(self.config.api, key, value)
        
        if 'agent' in data:
            for key, value in data['agent'].items():
                if hasattr(self.config.agent, key):
                    setattr(self.config.agent, key, value)
        
        if 'executor' in data:
            for key, value in data['executor'].items():
                if hasattr(self.config.executor, key):
                    setattr(self.config.executor, key, value)
        
        if 'monitoring' in data:
            for key, value in data['monitoring'].items():
                if hasattr(self.config.monitoring, key):
                    setattr(self.config.monitoring, key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key path.
        
        Args:
            key: Dot-separated key path (e.g., 'database.host')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        parts = key.split('.')
        obj = self.config
        
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return default
        
        return obj
    
    def set(self, key: str, value: Any):
        """
        Set configuration value by key path.
        
        Args:
            key: Dot-separated key path (e.g., 'database.host')
            value: Value to set
        """
        parts = key.split('.')
        obj = self.config
        
        for part in parts[:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                raise KeyError(f"Invalid config key: {key}")
        
        setattr(obj, parts[-1], value)
    
    def validate(self) -> List[str]:
        """
        Validate configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate environment
        if self.config.environment not in ['development', 'staging', 'production', 'test']:
            errors.append(f"Invalid environment: {self.config.environment}")
        
        # Validate LLM config
        if self.config.environment == 'production' and not self.config.llm.api_key:
            errors.append("LLM API key is required in production")
        
        if self.config.llm.max_tokens < 1:
            errors.append("LLM max_tokens must be positive")
        
        if not 0 <= self.config.llm.temperature <= 2:
            errors.append("LLM temperature must be between 0 and 2")
        
        # Validate NLP config
        if not 0 <= self.config.nlp.confidence_threshold <= 1:
            errors.append("NLP confidence_threshold must be between 0 and 1")
        
        # Validate API config
        if not 1024 <= self.config.api.port <= 65535:
            errors.append("API port must be between 1024 and 65535")
        
        if self.config.api.rate_limit_per_minute < 1:
            errors.append("API rate_limit_per_minute must be positive")
        
        # Validate Agent config
        if self.config.agent.max_workers < 1:
            errors.append("Agent max_workers must be positive")
        
        if not 0 <= self.config.agent.quality_threshold <= 1:
            errors.append("Agent quality_threshold must be between 0 and 1")
        
        # Validate Executor config
        if self.config.executor.changes_per_round < 1:
            errors.append("Executor changes_per_round must be positive")
        
        if not 0 <= self.config.executor.min_quality_score <= 1:
            errors.append("Executor min_quality_score must be between 0 and 1")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Configuration as dictionary
        """
        return asdict(self.config)
    
    def to_json(self, pretty: bool = True) -> str:
        """
        Convert configuration to JSON string.
        
        Args:
            pretty: Enable pretty printing
            
        Returns:
            JSON string
        """
        data = self.to_dict()
        if pretty:
            return json.dumps(data, indent=2)
        return json.dumps(data)
    
    def to_yaml(self) -> str:
        """
        Convert configuration to YAML string.
        
        Returns:
            YAML string
        """
        data = self.to_dict()
        return yaml.dump(data, default_flow_style=False)
    
    def save_to_file(self, path: str):
        """
        Save configuration to file.
        
        Args:
            path: File path (JSON or YAML based on extension)
        """
        with open(path, 'w') as f:
            if path.endswith('.json'):
                json.dump(self.to_dict(), f, indent=2)
            elif path.endswith(('.yml', '.yaml')):
                yaml.dump(self.to_dict(), f, default_flow_style=False)
            else:
                raise ValueError("File must have .json, .yml, or .yaml extension")
    
    def get_environment_config(self, env: str) -> SystemConfig:
        """
        Get configuration for specific environment.
        
        Args:
            env: Environment name
            
        Returns:
            Configuration for environment
        """
        config = copy.deepcopy(self.config)
        config.environment = env
        
        # Apply environment-specific overrides
        if env == 'production':
            config.debug = False
            config.monitoring.enabled = True
            config.monitoring.metrics_enabled = True
            config.api.rate_limit_enabled = True
            config.api.auth_enabled = True
        elif env == 'development':
            config.debug = True
            config.monitoring.log_level = 'DEBUG'
        elif env == 'test':
            config.database.database = 'test_db'
            config.llm.cache_enabled = False
        
        return config
    
    def __repr__(self) -> str:
        return f"ConfigManager(environment={self.config.environment}, loaded={self._loaded})"


# Global config instance
_config_manager = None


def get_config() -> ConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
        _config_manager.load_from_env()
    return _config_manager


def init_config(config_path: Optional[str] = None, environment: Optional[str] = None) -> ConfigManager:
    """
    Initialize global configuration.
    
    Args:
        config_path: Optional path to config file
        environment: Optional environment override
        
    Returns:
        Configured ConfigManager instance
    """
    global _config_manager
    _config_manager = ConfigManager(environment=environment)
    
    if config_path:
        _config_manager.load_from_file(config_path)
    else:
        _config_manager.load_from_env()
    
    # Validate configuration
    errors = _config_manager.validate()
    if errors:
        print("⚠ Configuration validation warnings:")
        for error in errors:
            print(f"  - {error}")
    
    return _config_manager


if __name__ == '__main__':
    # Demo usage
    print("Configuration Management System Demo")
    print("=" * 60)
    print()
    
    # Create config manager
    config = ConfigManager(environment='development')
    config.load_from_env()
    
    print("Current Configuration:")
    print(f"  Environment: {config.config.environment}")
    print(f"  Debug: {config.config.debug}")
    print(f"  LLM Model: {config.config.llm.default_model}")
    print(f"  API Port: {config.config.api.port}")
    print(f"  Agent Workers: {config.config.agent.max_workers}")
    print()
    
    # Validate
    errors = config.validate()
    if errors:
        print(f"Validation Errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✓ Configuration valid")
    
    print()
    print("Configuration as JSON:")
    print(config.to_json()[:500] + "...")
