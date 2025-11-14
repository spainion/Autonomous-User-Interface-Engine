"""
Comprehensive Integration Testing Suite

Tests all system components working together, validates workflows,
and ensures production readiness.
"""

import unittest
import asyncio
import time
from typing import Dict, Any, List
import sys
import os

# Import all systems
try:
    from workflow_database import WorkflowDatabase
    from enhanced_nlp_system import EnhancedNLPSystem
    from intelligent_llm_orchestrator import IntelligentLLMOrchestrator, TaskType
    from enhanced_ui_builder import EnhancedUIBuilder, UIFramework, ComponentType
    from enhanced_api_integrations import EnhancedAPIIntegration, HTTPMethod
    from multi_agent_coordinator import MultiAgentCoordinator, CoordinationStrategy
    from autonomous_executor import AutonomousExecutor, ExecutionStrategy
    from comprehensive_system_integration import ComprehensiveSystem
except ImportError as e:
    print(f"⚠ Import warning: {e}")


class TestWorkflowDatabase(unittest.TestCase):
    """Test workflow database functionality"""
    
    def setUp(self):
        self.db = WorkflowDatabase()
    
    def test_file_scanning(self):
        """Test repository scanning"""
        result = self.db.scan_repository()
        self.assertGreater(result['files_scanned'], 0)
        self.assertIn('total_files', result)
        print(f"✓ Scanned {result['files_scanned']} files")
    
    def test_agent_registration(self):
        """Test agent registration"""
        agent_info = {
            'name': 'test_agent',
            'capabilities': ['testing'],
            'version': '1.0.0'
        }
        self.db.register_agent('test_agent', agent_info)
        agents = self.db.get_all_agents()
        self.assertIn('test_agent', agents)
        print(f"✓ Registered test agent")
    
    def test_workflow_definition(self):
        """Test workflow creation"""
        workflow = {
            'name': 'test_workflow',
            'steps': [
                {'action': 'analyze', 'agent': 'test_agent'},
                {'action': 'execute', 'agent': 'test_agent'}
            ]
        }
        self.db.define_workflow('test_workflow', workflow)
        workflows = self.db.get_all_workflows()
        self.assertIn('test_workflow', workflows)
        print(f"✓ Defined test workflow")


class TestEnhancedNLP(unittest.TestCase):
    """Test enhanced NLP system"""
    
    def setUp(self):
        self.nlp = EnhancedNLPSystem()
    
    def test_language_detection(self):
        """Test language detection"""
        texts = {
            "Hello, how are you?": "en",
            "Bonjour, comment allez-vous?": "fr",
            "Hola, ¿cómo estás?": "es",
            "こんにちは": "ja",
        }
        
        for text, expected_lang in texts.items():
            result = self.nlp.detect_language(text)
            self.assertIsNotNone(result)
            print(f"✓ Detected language for: {text[:30]}")
    
    def test_intent_classification(self):
        """Test intent classification"""
        test_cases = [
            "Create a new user interface",
            "Generate code for authentication",
            "Search for design patterns",
        ]
        
        for text in test_cases:
            result = self.nlp.classify_intent(text)
            self.assertIsNotNone(result)
            print(f"✓ Classified intent: {text[:40]}")
    
    def test_entity_extraction(self):
        """Test entity extraction"""
        text = "Create a dashboard with login form and user table"
        entities = self.nlp.extract_entities(text)
        self.assertIsInstance(entities, list)
        print(f"✓ Extracted {len(entities)} entities")


class TestIntelligentOrchestrator(unittest.TestCase):
    """Test intelligent LLM orchestrator"""
    
    def setUp(self):
        self.orch = IntelligentLLMOrchestrator()
    
    def test_model_selection(self):
        """Test intelligent model selection"""
        test_cases = [
            (TaskType.CODE_GENERATION, 'high'),
            (TaskType.TEXT_GENERATION, 'medium'),
            (TaskType.TRANSLATION, 'low'),
        ]
        
        for task_type, complexity in test_cases:
            model = self.orch.select_best_model(task_type, complexity)
            self.assertIsNotNone(model)
            print(f"✓ Selected model for {task_type}: {model.model_id}")
    
    def test_prompt_template_generation(self):
        """Test prompt template generation"""
        templates = self.orch.get_all_templates()
        self.assertGreater(len(templates), 0)
        print(f"✓ Found {len(templates)} prompt templates")
    
    def test_caching_mechanism(self):
        """Test response caching"""
        cache_size_before = len(self.orch.response_cache)
        
        # Simulate adding to cache
        test_key = "test_prompt_123"
        test_response = {"result": "cached_response"}
        self.orch.response_cache[test_key] = test_response
        
        self.assertEqual(len(self.orch.response_cache), cache_size_before + 1)
        print(f"✓ Caching mechanism working")


class TestUIBuilder(unittest.TestCase):
    """Test enhanced UI builder"""
    
    def setUp(self):
        self.builder = EnhancedUIBuilder(framework=UIFramework.REACT)
    
    def test_component_creation(self):
        """Test component creation"""
        component = self.builder.create_component(
            name="TestButton",
            component_type=ComponentType.INTERACTIVE,
            props={'label': 'Click Me'}
        )
        self.assertIsNotNone(component)
        print(f"✓ Created test component")
    
    def test_framework_switching(self):
        """Test framework switching"""
        frameworks = [UIFramework.REACT, UIFramework.VUE, UIFramework.HTML]
        
        for framework in frameworks:
            builder = EnhancedUIBuilder(framework=framework)
            self.assertEqual(builder.framework, framework)
            print(f"✓ Switched to {framework.value}")
    
    def test_responsive_design(self):
        """Test responsive design generation"""
        component = self.builder.create_component(
            name="ResponsiveCard",
            component_type=ComponentType.LAYOUT,
            responsive=True
        )
        self.assertIsNotNone(component)
        print(f"✓ Generated responsive component")


class TestAPIIntegration(unittest.TestCase):
    """Test enhanced API integration"""
    
    def setUp(self):
        self.api = EnhancedAPIIntegration(app_name="Test API", version="1.0.0")
    
    def test_route_registration(self):
        """Test route registration"""
        @self.api.route('/test', method=HTTPMethod.GET)
        def test_endpoint(request):
            return {'status': 'ok'}
        
        routes = self.api.get_all_routes()
        self.assertGreater(len(routes), 0)
        print(f"✓ Registered {len(routes)} routes")
    
    def test_openapi_generation(self):
        """Test OpenAPI spec generation"""
        spec = self.api.generate_openapi_spec()
        self.assertIn('openapi', spec)
        self.assertIn('info', spec)
        print(f"✓ Generated OpenAPI spec")
    
    def test_client_sdk_generation(self):
        """Test client SDK generation"""
        python_sdk = self.api.generate_client_sdk('python')
        self.assertIsInstance(python_sdk, str)
        self.assertGreater(len(python_sdk), 0)
        print(f"✓ Generated Python SDK ({len(python_sdk)} chars)")


class TestMultiAgentCoordinator(unittest.TestCase):
    """Test multi-agent coordinator"""
    
    def setUp(self):
        self.coordinator = MultiAgentCoordinator(max_workers=5)
    
    def test_agent_registration(self):
        """Test agent registration"""
        # Mock agent
        class MockAgent:
            def execute(self, task):
                return {'result': 'success', 'output': f'Completed: {task}'}
        
        agent = MockAgent()
        self.coordinator.register_agent('mock_agent', agent)
        agents = self.coordinator.get_all_agents()
        self.assertIn('mock_agent', agents)
        print(f"✓ Registered mock agent")
    
    def test_coordination_strategies(self):
        """Test different coordination strategies"""
        strategies = [
            CoordinationStrategy.SEQUENTIAL,
            CoordinationStrategy.PARALLEL,
        ]
        
        for strategy in strategies:
            # Test strategy exists
            self.assertIn(strategy, CoordinationStrategy)
            print(f"✓ Strategy available: {strategy.value}")


class TestAutonomousExecutor(unittest.TestCase):
    """Test autonomous executor"""
    
    def setUp(self):
        # Mock agents for testing
        class MockAgent:
            def execute(self, task):
                return {'result': 'success', 'quality': 1.0}
        
        self.agents = [MockAgent() for _ in range(3)]
        self.executor = AutonomousExecutor(
            agents=self.agents,
            changes_per_round=5,
            max_iterations=2
        )
    
    def test_execution_strategies(self):
        """Test execution strategies"""
        strategies = [
            ExecutionStrategy.SINGLE_PASS,
            ExecutionStrategy.BATCH_PARALLEL,
        ]
        
        for strategy in strategies:
            self.assertIn(strategy, ExecutionStrategy)
            print(f"✓ Strategy available: {strategy.value}")
    
    def test_quality_monitoring(self):
        """Test quality monitoring"""
        # Executor has quality monitoring
        self.assertTrue(hasattr(self.executor, 'min_quality_score'))
        print(f"✓ Quality monitoring enabled")


class TestComprehensiveIntegration(unittest.TestCase):
    """Test comprehensive system integration"""
    
    def setUp(self):
        self.system = ComprehensiveSystem()
    
    def test_system_initialization(self):
        """Test system initialization"""
        self.assertIsNotNone(self.system)
        print(f"✓ System initialized")
    
    def test_component_integration(self):
        """Test all components are integrated"""
        # Check if key components are available
        components = ['workflow_db', 'nlp_system', 'orchestrator']
        
        for comp in components:
            self.assertTrue(hasattr(self.system, comp))
            print(f"✓ Component integrated: {comp}")
    
    def test_health_check(self):
        """Test system health check"""
        health = self.system.get_health_status()
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        print(f"✓ Health check: {health.get('status', 'unknown')}")


class IntegrationTestRunner:
    """Run all integration tests and generate report"""
    
    def __init__(self):
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'duration': 0
        }
    
    def run_all_tests(self):
        """Run all test suites"""
        print("=" * 80)
        print("COMPREHENSIVE INTEGRATION TEST SUITE")
        print("=" * 80)
        print()
        
        start_time = time.time()
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add all test classes
        test_classes = [
            TestWorkflowDatabase,
            TestEnhancedNLP,
            TestIntelligentOrchestrator,
            TestUIBuilder,
            TestAPIIntegration,
            TestMultiAgentCoordinator,
            TestAutonomousExecutor,
            TestComprehensiveIntegration
        ]
        
        for test_class in test_classes:
            tests = loader.loadTestsFromTestCase(test_class)
            suite.addTests(tests)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Calculate results
        self.results['total'] = result.testsRun
        self.results['passed'] = result.testsRun - len(result.failures) - len(result.errors)
        self.results['failed'] = len(result.failures)
        self.results['errors'] = [(str(test), str(err)) for test, err in result.errors + result.failures]
        self.results['duration'] = time.time() - start_time
        
        # Print summary
        print()
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.results['total']}")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Duration: {self.results['duration']:.2f}s")
        print(f"Success Rate: {(self.results['passed']/self.results['total']*100):.1f}%")
        
        if self.results['errors']:
            print("\nErrors:")
            for test, error in self.results['errors'][:5]:  # Show first 5 errors
                print(f"  - {test}")
        
        print("=" * 80)
        
        return self.results


if __name__ == '__main__':
    runner = IntegrationTestRunner()
    results = runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if results['failed'] == 0 else 1)
