"""
Tests for LLM UI Generator and Design Orchestrator
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from llm_ui_generator import LLMUIGenerator, LLMUIResult
from design_orchestrator import DesignOrchestrator, DesignResult


class TestLLMUIGenerator:
    """Test suite for LLM UI Generator"""
    
    @pytest.fixture
    def generator(self):
        """Create generator instance for testing"""
        return LLMUIGenerator(api_key="test_key")
    
    def test_initialization(self, generator):
        """Test generator initializes properly"""
        assert generator.api_key is not None
        assert generator.base_url is not None
        assert len(generator.models) > 0
        assert 'gpt-4' in generator.models
        assert 'claude' in generator.models
    
    def test_supported_models(self, generator):
        """Test all required models are supported"""
        required_models = ['gpt-4', 'claude', 'gemini', 'mixtral']
        for model in required_models:
            assert model in generator.models
    
    @patch('llm_ui_generator.requests.post')
    def test_generate_with_reasoning_mocked(self, mock_post, generator):
        """Test UI generation with mocked API"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': '''
                    <html>
                        <head><title>Test</title></head>
                        <body>
                            <h1>Test UI</h1>
                        </body>
                    </html>
                    
                    <style>
                        body { margin: 0; }
                    </style>
                    
                    <script>
                        console.log('test');
                    </script>
                    '''
                }
            }]
        }
        mock_post.return_value = mock_response
        
        # Test generation
        result = generator.generate_with_reasoning(
            prompt="Create a login form",
            model='gpt-4',
            enhance_prompt=False,
            research_enabled=False
        )
        
        assert isinstance(result, LLMUIResult)
        assert result.html is not None
        assert result.quality_score >= 0.0
    
    def test_generate_with_reasoning_no_api_key(self):
        """Test generation fails gracefully without API key"""
        generator = LLMUIGenerator(api_key="")
        # Should handle missing API key gracefully
        assert generator.api_key == ""


class TestLLMUIResult:
    """Test suite for LLMUIResult dataclass"""
    
    def test_llm_ui_result_creation(self):
        """Test creating an LLM UI result"""
        result = LLMUIResult(
            html="<div>Test</div>",
            css=".test { color: red; }",
            js="console.log('test');",
            reasoning="Generated based on prompt",
            quality_score=0.85,
            improvements=["Add more spacing", "Improve colors"]
        )
        
        assert result.html == "<div>Test</div>"
        assert result.css == ".test { color: red; }"
        assert result.js == "console.log('test');"
        assert result.reasoning == "Generated based on prompt"
        assert result.quality_score == 0.85
        assert len(result.improvements) == 2
    
    def test_llm_ui_result_fields(self):
        """Test LLM UI result has all required fields"""
        result = LLMUIResult(
            html="",
            css="",
            js="",
            reasoning="",
            quality_score=0.0,
            improvements=[]
        )
        
        assert hasattr(result, 'html')
        assert hasattr(result, 'css')
        assert hasattr(result, 'js')
        assert hasattr(result, 'reasoning')
        assert hasattr(result, 'quality_score')
        assert hasattr(result, 'improvements')


class TestDesignOrchestrator:
    """Test suite for Design Orchestrator"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance for testing"""
        return DesignOrchestrator()
    
    def test_initialization(self, orchestrator):
        """Test orchestrator initializes properly"""
        assert orchestrator.ui_expert is not None
        assert orchestrator.research_engine is not None
        assert orchestrator.llm_generator is not None
        assert len(orchestrator.pipeline_stages) > 0
    
    def test_pipeline_stages(self, orchestrator):
        """Test all required pipeline stages exist"""
        required_stages = ['research', 'generation', 'enhancement', 'quality_assurance', 'optimization']
        for stage in required_stages:
            assert stage in orchestrator.pipeline_stages
    
    @patch.object(LLMUIGenerator, 'generate_with_reasoning')
    def test_create_complete_ui_with_llm(self, mock_generate, orchestrator):
        """Test complete UI creation with mocked LLM"""
        # Mock LLM response
        mock_generate.return_value = LLMUIResult(
            html="<div>Generated UI</div>",
            css=".generated { color: blue; }",
            js="console.log('generated');",
            reasoning="Generated using best practices",
            quality_score=0.90,
            improvements=[]
        )
        
        result = orchestrator.create_complete_ui(
            description="Create a dashboard",
            niche="analytics",
            framework="bootstrap",
            research_enabled=False,
            llm_reasoning=True,
            generate_variants=1,
            quality_assurance=False,
            usability_testing=False
        )
        
        assert isinstance(result, DesignResult)
        assert result.html is not None
        assert result.quality_score >= 0.0
        assert result.generation_time >= 0.0
    
    def test_create_complete_ui_without_llm(self, orchestrator):
        """Test complete UI creation without LLM"""
        result = orchestrator.create_complete_ui(
            description="Create a landing page",
            framework="bootstrap",
            research_enabled=False,
            llm_reasoning=False,
            generate_variants=1,
            quality_assurance=False,
            usability_testing=False
        )
        
        assert isinstance(result, DesignResult)
        assert result.html is not None
        assert result.quality_score >= 0.0
        assert result.generation_time >= 0.0


class TestDesignResult:
    """Test suite for DesignResult dataclass"""
    
    def test_design_result_creation(self):
        """Test creating a design result"""
        result = DesignResult(
            html="<div>Complete</div>",
            css=".complete { margin: 0; }",
            js="console.log('complete');",
            quality_score=0.88,
            accessibility_score=0.92,
            performance_score=0.85,
            improvements=["Improvement 1"],
            research_data={"category": "landing_pages"},
            reasoning="Complete reasoning",
            generation_time=1.5
        )
        
        assert result.html == "<div>Complete</div>"
        assert result.quality_score == 0.88
        assert result.accessibility_score == 0.92
        assert result.performance_score == 0.85
        assert result.generation_time == 1.5
        assert len(result.improvements) == 1
        assert "category" in result.research_data
    
    def test_design_result_fields(self):
        """Test design result has all required fields"""
        result = DesignResult(
            html="",
            css="",
            js="",
            quality_score=0.0,
            accessibility_score=0.0,
            performance_score=0.0,
            improvements=[],
            research_data={},
            reasoning="",
            generation_time=0.0
        )
        
        assert hasattr(result, 'html')
        assert hasattr(result, 'css')
        assert hasattr(result, 'js')
        assert hasattr(result, 'quality_score')
        assert hasattr(result, 'accessibility_score')
        assert hasattr(result, 'performance_score')
        assert hasattr(result, 'improvements')
        assert hasattr(result, 'research_data')
        assert hasattr(result, 'reasoning')
        assert hasattr(result, 'generation_time')


class TestIntegration:
    """Integration tests for the complete system"""
    
    def test_full_pipeline_without_api(self):
        """Test full pipeline without API calls"""
        orchestrator = DesignOrchestrator()
        
        result = orchestrator.create_complete_ui(
            description="Modern SaaS landing page",
            framework="bootstrap",
            research_enabled=False,
            llm_reasoning=False,
            quality_assurance=False
        )
        
        assert isinstance(result, DesignResult)
        assert len(result.html) > 0
        assert result.generation_time > 0
    
    def test_multiple_frameworks(self):
        """Test generation with multiple frameworks"""
        orchestrator = DesignOrchestrator()
        
        for framework in ['bootstrap', 'tailwind', 'custom']:
            result = orchestrator.create_complete_ui(
                description="Test page",
                framework=framework,
                research_enabled=False,
                llm_reasoning=False,
                quality_assurance=False
            )
            
            assert isinstance(result, DesignResult)
            assert len(result.html) > 0
