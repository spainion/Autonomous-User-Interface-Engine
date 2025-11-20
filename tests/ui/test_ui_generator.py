"""Tests for UI generation functionality."""

import pytest


class TestUIGenerator:
    """Test suite for UI generator."""

    def test_ui_generator_initialization(self):
        """Test UI generator initializes."""
        try:
            from llm_ui_generator import LLMUIGenerator
            generator = LLMUIGenerator()
            assert generator is not None
        except ImportError:
            pytest.skip("LLMUIGenerator not available")

    def test_ui_generation_basic(self):
        """Test basic UI generation."""
        try:
            from llm_ui_generator import LLMUIGenerator
            generator = LLMUIGenerator()
            # Basic test that it has expected methods
            assert hasattr(generator, 'generate_with_reasoning')
        except ImportError:
            pytest.skip("LLMUIGenerator not available")
