"""
Agents package - Context-aware agents for the Autonomous UI Engine.

All agents use the shared Context Engine for memory and information.

Enhanced agents provide:
- Network API integration
- Batch processing
- Iterative enhancements
- Cross-compatibility optimization

Self-Enhancing agents add:
- Self-learning from experiences
- Self-programming new tools
- Enhanced reasoning and planning
- Improved coordination
"""

from .base_agent import BaseAgent
from .concrete_agents import CodexAgent, UIDesignerAgent, ReasoningAgent
from .enhanced_agents import EnhancedBaseAgent
from .enhanced_concrete_agents import (
    EnhancedCodexAgent,
    EnhancedUIDesignerAgent,
    EnhancedReasoningAgent
)
from .self_enhancing_agent import SelfEnhancingAgent
from .self_enhancing_concrete_agents import (
    SelfEnhancingCodexAgent,
    SelfEnhancingUIDesignerAgent,
    SelfEnhancingReasoningAgent
)

__all__ = [
    'BaseAgent',
    'CodexAgent',
    'UIDesignerAgent', 
    'ReasoningAgent',
    'EnhancedBaseAgent',
    'EnhancedCodexAgent',
    'EnhancedUIDesignerAgent',
    'EnhancedReasoningAgent',
    'SelfEnhancingAgent',
    'SelfEnhancingCodexAgent',
    'SelfEnhancingUIDesignerAgent',
    'SelfEnhancingReasoningAgent'
]

