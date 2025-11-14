"""
Demo: Intelligent LLM Orchestration with Enhanced NLP

This demo showcases the intelligent orchestration system integrated
with the enhanced NLP interpreter for superior results.
"""

import os
import json
from intelligent_llm_orchestrator import IntelligentLLMOrchestrator, TaskType
from enhanced_nlp_system import EnhancedNLPSystem

# Optional: Import context engine and agents if available
try:
    from agent_init import init_agent_system
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False


def demo_model_selection():
    """Demo 1: Intelligent Model Selection"""
    print("=" * 80)
    print("DEMO 1: Intelligent Model Selection")
    print("=" * 80)
    print("\nShowing how the orchestrator selects the best model for different tasks:\n")
    
    orchestrator = IntelligentLLMOrchestrator()
    
    test_cases = [
        (TaskType.CODE_GENERATION, 'high', None),
        (TaskType.CODE_GENERATION, 'low', None),
        (TaskType.UI_DESIGN, 'medium', None),
        (TaskType.REASONING, 'high', None),
        (TaskType.TRANSLATION, 'low', None),
        (TaskType.CODE_GENERATION, 'high', 0.005),  # With budget constraint
    ]
    
    for task, complexity, budget in test_cases:
        model_key = orchestrator.select_best_model(task, complexity, budget)
        model = orchestrator.models[model_key]
        
        budget_str = f", Budget: ${budget}" if budget else ""
        print(f"Task: {task.value:20s} | Complexity: {complexity:6s}{budget_str}")
        print(f"  → Selected: {model.display_name:20s} | Cost: ${model.cost_per_1k_tokens:.5f}/1K tokens")
        print()


def demo_prompt_templates():
    """Demo 2: Advanced Prompt Templates"""
    print("\n" + "=" * 80)
    print("DEMO 2: Advanced Prompt Templates")
    print("=" * 80)
    print("\nDifferent prompting strategies for different tasks:\n")
    
    orchestrator = IntelligentLLMOrchestrator()
    
    examples = [
        {
            'name': 'Chain-of-Thought (CoT) - Code Generation',
            'template_id': 'code_generation_cot',
            'variables': {
                'task_description': 'Create a binary search algorithm in Python'
            }
        },
        {
            'name': 'Tree-of-Thought (ToT) - Reasoning',
            'template_id': 'reasoning_tot',
            'variables': {
                'problem': 'How to optimize database queries for a high-traffic application'
            }
        },
        {
            'name': 'Instruction Following - UI Design',
            'template_id': 'ui_design_detailed',
            'variables': {
                'requirements': 'Admin dashboard with user management',
                'framework': 'bootstrap',
                'style': 'modern'
            }
        }
    ]
    
    for example in examples:
        print(f"📋 {example['name']}")
        print("-" * 80)
        
        system_prompt, user_prompt = orchestrator.build_prompt(
            example['template_id'],
            example['variables']
        )
        
        print(f"System Prompt: {system_prompt[:150]}...")
        print(f"User Prompt: {user_prompt[:200]}...")
        print()


def demo_basic_orchestration():
    """Demo 3: Basic Orchestration (Single Model)"""
    print("\n" + "=" * 80)
    print("DEMO 3: Basic Orchestration (Single Model)")
    print("=" * 80)
    print("\nDemonstrating single-model orchestration with intelligent prompting:\n")
    
    # Note: This requires an actual API key to execute
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("⚠ OPENROUTER_API_KEY not set - Showing structure only")
        print("\nWould execute:")
        print("  1. Select best model for CODE_GENERATION (medium complexity)")
        print("  2. Build Chain-of-Thought prompt")
        print("  3. Execute request with caching")
        print("  4. Return structured response with metrics")
        return
    
    orchestrator = IntelligentLLMOrchestrator(api_key=api_key)
    
    # Select model
    model_key = orchestrator.select_best_model(
        TaskType.CODE_GENERATION,
        complexity='medium'
    )
    
    print(f"Selected model: {orchestrator.models[model_key].display_name}")
    
    # Build prompt
    system_prompt, user_prompt = orchestrator.build_prompt(
        'code_generation_cot',
        {'task_description': 'Create a function to validate email addresses'}
    )
    
    print("\nExecuting request...")
    print("(This would call OpenRouter API if credentials are valid)")
    
    # In real usage:
    # response = orchestrator.execute_llm_request(
    #     model_key=model_key,
    #     system_prompt=system_prompt,
    #     user_prompt=user_prompt
    # )
    # print(f"\nResponse: {response.content[:300]}...")
    # print(f"Cost: ${response.cost:.4f}")
    # print(f"Tokens: {response.tokens_used}")


def demo_multi_model_consensus():
    """Demo 4: Multi-Model Consensus"""
    print("\n" + "=" * 80)
    print("DEMO 4: Multi-Model Consensus")
    print("=" * 80)
    print("\nUsing multiple models for higher confidence:\n")
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("⚠ OPENROUTER_API_KEY not set - Showing structure only")
        print("\nWould execute:")
        print("  1. Select 3 models suitable for REASONING")
        print("  2. Send same prompt to all models in parallel")
        print("  3. Collect all responses")
        print("  4. Synthesize results")
        print("  5. Calculate consensus confidence")
        print("\nExpected models: GPT-4 Turbo, Claude 3 Opus, Gemini Pro")
        return
    
    orchestrator = IntelligentLLMOrchestrator(api_key=api_key)
    
    print("Consensus orchestration would use 3 models:")
    print("  1. GPT-4 Turbo (OpenAI)")
    print("  2. Claude 3 Opus (Anthropic)")
    print("  3. Gemini Pro (Google)")
    print("\nEach model provides its perspective, then results are synthesized.")
    
    # In real usage:
    # result = orchestrator.orchestrate_with_consensus(
    #     task_type=TaskType.REASONING,
    #     template_id='reasoning_tot',
    #     variables={'problem': 'Best practices for microservices architecture'},
    #     num_models=3
    # )
    # print(f"\nSynthesized result: {result.synthesized_result[:300]}...")
    # print(f"Confidence: {result.confidence:.0%}")
    # print(f"Total cost: ${result.total_cost:.4f}")


def demo_nlp_integration():
    """Demo 5: NLP Integration with Orchestration"""
    print("\n" + "=" * 80)
    print("DEMO 5: Enhanced NLP with Orchestration")
    print("=" * 80)
    print("\nIntegrating orchestration with NLP interpretation:\n")
    
    # Initialize with orchestration
    nlp = EnhancedNLPSystem(
        context_engine=None,
        use_orchestrator=True
    )
    
    # Check if orchestrator is available
    if nlp.orchestrator:
        print("✓ Orchestrator successfully integrated with NLP system")
        print(f"  Available models: {len(nlp.orchestrator.models)}")
        print(f"  Prompt templates: {len(nlp.orchestrator.prompt_templates)}")
    else:
        print("⚠ Orchestrator not available (API key may be missing)")
        return
    
    # Test interpretation
    test_cases = [
        "Create a modern e-commerce website with shopping cart and checkout",
        "Optimize the database queries for better performance",
        "Design a RESTful API for user authentication"
    ]
    
    print("\nTest cases:")
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i}. Input: {test_input}")
        
        # Basic interpretation (no API call)
        interpretation = nlp._basic_interpretation(test_input)
        
        print(f"   Detected Intent: {interpretation.intent.value}")
        print(f"   Language: {interpretation.language.value}")
        print(f"   Components: {interpretation.semantic_structure.get('components', [])}")
        
        # Determine which model would be selected
        intent_to_task = {
            'create_ui': TaskType.UI_DESIGN,
            'modify_ui': TaskType.UI_DESIGN,
            'generate_code': TaskType.CODE_GENERATION,
            'optimize': TaskType.CODE_ANALYSIS
        }
        
        task_type = TaskType.UI_DESIGN
        for key, val in intent_to_task.items():
            if key in interpretation.intent.value:
                task_type = val
                break
        
        model_key = nlp.orchestrator.select_best_model(task_type, 'medium')
        print(f"   Would use model: {nlp.orchestrator.models[model_key].display_name}")


def demo_performance_metrics():
    """Demo 6: Performance Metrics"""
    print("\n" + "=" * 80)
    print("DEMO 6: Performance Metrics & Optimization")
    print("=" * 80)
    print("\nTracking orchestration performance:\n")
    
    orchestrator = IntelligentLLMOrchestrator(cache_enabled=True)
    
    # Simulate some metrics
    orchestrator.metrics['total_requests'] = 50
    orchestrator.metrics['cache_hits'] = 30
    orchestrator.metrics['total_cost'] = 0.245
    orchestrator.metrics['model_usage'] = {
        'gpt-4-turbo': 20,
        'claude-3-sonnet': 15,
        'gpt-3.5-turbo': 15
    }
    
    metrics = orchestrator.get_metrics()
    
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Cache Hits: {metrics['cache_hits']}")
    print(f"Cache Hit Rate: {metrics['cache_hit_rate']:.1%}")
    print(f"Total Cost: ${metrics['total_cost']:.4f}")
    print(f"Avg Cost per Request: ${metrics['avg_cost_per_request']:.4f}")
    print(f"\nModel Usage:")
    for model, count in metrics['model_usage'].items():
        print(f"  {model:20s}: {count:3d} requests ({count/metrics['total_requests']*100:.1f}%)")
    
    print("\n💡 Optimization Tips:")
    if metrics['cache_hit_rate'] > 0.5:
        print("  ✓ Excellent cache hit rate! You're saving on API costs.")
    else:
        print("  ⚠ Low cache hit rate. Consider pre-warming cache with common queries.")
    
    if metrics['avg_cost_per_request'] > 0.01:
        print("  ⚠ High average cost. Consider using cheaper models for simple tasks.")
    else:
        print("  ✓ Good cost efficiency!")


def demo_complete_workflow():
    """Demo 7: Complete Workflow Example"""
    print("\n" + "=" * 80)
    print("DEMO 7: Complete Workflow (End-to-End)")
    print("=" * 80)
    print("\nComplete workflow from input to output:\n")
    
    # Initialize full system if available
    context_engine = None
    if AGENTS_AVAILABLE:
        try:
            print("Initializing agent system...")
            context_engine, agents = init_agent_system()
            print("✓ Agent system initialized")
        except Exception as e:
            print(f"⚠ Agent system not available: {e}")
    
    # Initialize NLP with orchestration
    print("Initializing NLP system with orchestration...")
    nlp = EnhancedNLPSystem(
        context_engine=context_engine,
        use_orchestrator=True
    )
    
    # Test input
    user_input = "Create a responsive dashboard with data visualization charts, user management table, and real-time notifications"
    
    print(f"\n📝 User Input:")
    print(f"  \"{user_input}\"\n")
    
    print("🔄 Processing Pipeline:")
    print("  1. Language Detection")
    print("  2. Intent Classification")
    print("  3. Entity Extraction")
    print("  4. Model Selection")
    print("  5. Intelligent Prompting")
    print("  6. Result Generation")
    
    # Interpret (without actual API call)
    interpretation = nlp._basic_interpretation(user_input)
    
    print(f"\n📊 Results:")
    print(f"  Language: {interpretation.language.value}")
    print(f"  Intent: {interpretation.intent.value}")
    print(f"  Confidence: {interpretation.confidence:.0%}")
    print(f"  Entities Found: {len(interpretation.entities)}")
    print(f"  Components: {', '.join(interpretation.semantic_structure.get('components', []))}")
    
    if nlp.orchestrator:
        # Show which model would be used
        task_type = TaskType.UI_DESIGN
        model_key = nlp.orchestrator.select_best_model(task_type, 'medium')
        model = nlp.orchestrator.models[model_key]
        
        print(f"\n🤖 Model Selection:")
        print(f"  Selected: {model.display_name}")
        print(f"  Provider: {model.provider}")
        print(f"  Cost: ${model.cost_per_1k_tokens:.5f} per 1K tokens")
        print(f"  Strategy: Instruction Following (Detailed UI Design)")
        
        print(f"\n💭 Suggested Actions:")
        for i, action in enumerate(interpretation.suggested_actions, 1):
            print(f"  {i}. {action['action']} (priority: {action['priority']})")
    
    print("\n✅ Workflow complete!")


def main():
    """Run all demos"""
    print("\n" + "🚀" * 40)
    print("INTELLIGENT LLM ORCHESTRATION - COMPREHENSIVE DEMO")
    print("🚀" * 40 + "\n")
    
    demos = [
        ("Model Selection", demo_model_selection),
        ("Prompt Templates", demo_prompt_templates),
        ("Basic Orchestration", demo_basic_orchestration),
        ("Multi-Model Consensus", demo_multi_model_consensus),
        ("NLP Integration", demo_nlp_integration),
        ("Performance Metrics", demo_performance_metrics),
        ("Complete Workflow", demo_complete_workflow),
    ]
    
    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Demo '{name}' error: {e}")
    
    print("\n" + "=" * 80)
    print("ALL DEMOS COMPLETE!")
    print("=" * 80)
    print("\n📚 For more information, see INTELLIGENT_ORCHESTRATION.md")
    print("\n" + "🚀" * 40 + "\n")


if __name__ == "__main__":
    main()
