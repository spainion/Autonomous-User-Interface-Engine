"""Tests for base agent functionality."""

import pytest


class TestBaseAgent:
    """Test suite for BaseAgent."""

    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        try:
            from agents.base_agent import BaseAgent
            agent = BaseAgent(name="TestAgent")
            assert agent is not None
            assert agent.name == "TestAgent"
        except ImportError:
            pytest.skip("BaseAgent not available")

    def test_agent_basic_functionality(self):
        """Test agent basic functionality."""
        try:
            from agents.base_agent import BaseAgent
            agent = BaseAgent(name="TestAgent")
            assert hasattr(agent, 'name')
        except ImportError:
            pytest.skip("BaseAgent not available")
