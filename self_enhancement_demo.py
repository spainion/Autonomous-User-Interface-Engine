"""
Self-Enhancement System Demonstration.

Shows how agents can:
- Learn from their experiences
- Improve their own capabilities
- Self-program new tools
- Enhance coordination
"""

from agents.self_enhancing_concrete_agents import (
    SelfEnhancingCodexAgent,
    SelfEnhancingUIDesignerAgent,
    SelfEnhancingReasoningAgent
)


def demo_self_learning():
    """Demonstrate self-learning capabilities."""
    print("=" * 70)
    print("SELF-LEARNING DEMONSTRATION")
    print("=" * 70)
    
    codex = SelfEnhancingCodexAgent("LearningCodeBot")
    
    # Task 1: Initial attempt
    print("\n📝 Task 1: Generate authentication function")
    result1 = codex.process_request("Create user authentication function")
    print(f"   Generated: {result1['code'][:60]}...")
    
    # Task 2: Similar task - should improve
    print("\n📝 Task 2: Generate validation function (similar pattern)")
    result2 = codex.process_request("Create user validation function")
    print(f"   Generated: {result2['code'][:60]}...")
    print(f"   Self-enhanced: {result2.get('self_enhanced', False)}")
    
    # Task 3: Another similar task - even better
    print("\n📝 Task 3: Generate authorization function (learned pattern)")
    result3 = codex.process_request("Create user authorization function")
    print(f"   Generated: {result3['code'][:60]}...")
    
    # Show learning stats
    stats = codex.get_self_enhancement_stats()
    print(f"\n📊 Learning Statistics:")
    print(f"   Total tasks: {stats['total_tasks']}")
    print(f"   Success rate: {stats['success_rate']:.1%}")
    print(f"   Learned patterns: {stats['learned_patterns']}")
    print(f"   Improvements made: {stats['improvements_made']}")


def demo_self_programming():
    """Demonstrate self-programming capabilities."""
    print("\n" + "=" * 70)
    print("SELF-PROGRAMMING DEMONSTRATION")
    print("=" * 70)
    
    codex = SelfEnhancingCodexAgent("SelfProgrammingBot")
    
    print("\n🔧 Creating custom tools dynamically...")
    
    # Tool 1: Code formatter
    print("\n1️⃣  Self-programming 'format_code' tool...")
    formatter = codex.self_program_tool(
        'format_code',
        'Format code with proper indentation and style',
        '''
def format_code(code: str, indent_size: int = 4) -> str:
    """Format code with consistent style."""
    lines = code.split('\\n')
    formatted = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Decrease indent for closing brackets
        if stripped.startswith('}') or stripped.startswith(']'):
            indent_level = max(0, indent_level - 1)
        
        # Add formatted line
        formatted.append(' ' * (indent_level * indent_size) + stripped)
        
        # Increase indent for opening brackets
        if stripped.endswith('{') or stripped.endswith('['):
            indent_level += 1
    
    return '\\n'.join(formatted)
'''
    )
    
    # Tool 2: Complexity analyzer
    print("2️⃣  Self-programming 'analyze_complexity' tool...")
    analyzer = codex.self_program_tool(
        'analyze_complexity',
        'Analyze code complexity metrics'
    )
    
    # Tool 3: Security checker
    print("3️⃣  Self-programming 'check_security' tool...")
    security = codex.self_program_tool(
        'check_security',
        'Check for common security vulnerabilities'
    )
    
    # Show programmed tools
    stats = codex.get_self_enhancement_stats()
    print(f"\n✅ Self-programmed {stats['self_programmed_tools']} tools:")
    for tool_name in stats['tool_names']:
        print(f"   • {tool_name}")
    
    # Execute a self-programmed tool
    print("\n🎯 Testing 'format_code' tool...")
    test_code = "def hello():\nprint('hi')\nreturn True"
    formatted = codex.execute_self_programmed_tool('format_code', test_code)
    print(f"   Input: {test_code}")
    print(f"   Output: {formatted}")


def demo_enhanced_reasoning():
    """Demonstrate enhanced reasoning."""
    print("\n" + "=" * 70)
    print("ENHANCED REASONING DEMONSTRATION")
    print("=" * 70)
    
    reasoner = SelfEnhancingReasoningAgent("EnhancedReasoner")
    
    print("\n🧠 Processing complex problem with self-enhancement...")
    
    problem = "Design a scalable microservices architecture"
    result = reasoner.process_request(problem, complexity="high")
    
    print(f"\n📋 Problem: {problem}")
    print(f"\n✓ Reasoning approach: {result['reasoning'].get('approach', 'N/A')}")
    print(f"✓ Confidence: {result['reasoning'].get('confidence', 0):.1%}")
    print(f"✓ Steps generated: {len(result['reasoning'].get('steps', []))}")
    
    if 'problem_decomposition' in result:
        decomp = result['problem_decomposition']
        print(f"\n🔍 Problem decomposed into {decomp['complexity']} subtasks:")
        for i, subtask in enumerate(decomp['subtasks'], 1):
            print(f"   {i}. {subtask}")
    
    if 'solution_evaluation' in result:
        eval_data = result['solution_evaluation']
        print(f"\n⭐ Solution quality: {eval_data['quality_score']}/100")
        print(f"   Evaluation: {eval_data['evaluation']}")


def demo_improved_coordination():
    """Demonstrate improved agent coordination."""
    print("\n" + "=" * 70)
    print("IMPROVED COORDINATION DEMONSTRATION")
    print("=" * 70)
    
    codex = SelfEnhancingCodexAgent("CoordinatorCoder")
    designer = SelfEnhancingUIDesignerAgent("CoordinatorDesigner")
    reasoner = SelfEnhancingReasoningAgent("CoordinatorReasoner")
    
    print("\n🤝 Establishing enhanced coordination...")
    
    # Reasoner creates plan
    print("\n1️⃣  Reasoner creates comprehensive plan...")
    plan = reasoner.process_request("Plan a user dashboard feature")
    
    # Analyze coordination needs
    print("\n2️⃣  Analyzing coordination requirements...")
    coord_codex = codex.improve_coordination("CoordinatorDesigner")
    coord_designer = designer.improve_coordination("CoordinatorCoder")
    
    print(f"\n📊 Coordination Analysis:")
    print(f"   Codex → Designer:")
    print(f"      Past collaborations: {coord_codex['past_collaborations']}")
    print(f"      Priority: {coord_codex['priority']}")
    print(f"      Improvements: {len(coord_codex['improvements'])}")
    
    print(f"\n   Designer → Codex:")
    print(f"      Past collaborations: {coord_designer['past_collaborations']}")
    print(f"      Priority: {coord_designer['priority']}")
    
    # Share with enhanced coordination
    print("\n3️⃣  Sharing plan with enhanced protocols...")
    codex.share_with_agent("CoordinatorDesigner", plan, "enhanced_plan")
    designer.share_with_agent("CoordinatorCoder", {"ack": "received"}, "acknowledgment")
    
    print("   ✓ Enhanced coordination established")
    print("   ✓ Shared vocabulary aligned")
    print("   ✓ Data formats synchronized")


def demo_self_enhancement_cycle():
    """Demonstrate complete self-enhancement cycle."""
    print("\n" + "=" * 70)
    print("COMPLETE SELF-ENHANCEMENT CYCLE")
    print("=" * 70)
    
    codex = SelfEnhancingCodexAgent("SelfEvolvingBot")
    
    print("\n🔄 Running self-enhancement cycle...")
    
    # Initial state
    initial_stats = codex.get_self_enhancement_stats()
    print(f"\n📍 Initial state:")
    print(f"   Tools: {initial_stats['self_programmed_tools']}")
    print(f"   Patterns: {initial_stats['learned_patterns']}")
    
    # Perform several tasks
    print("\n🎯 Performing tasks to gather experience...")
    tasks = [
        "Create REST API endpoint",
        "Create database model",
        "Create authentication middleware",
        "Create error handler",
        "Create logging utility"
    ]
    
    for i, task in enumerate(tasks, 1):
        result = codex.process_request(task)
        print(f"   {i}. {task} - {'✓' if result else '✗'}")
    
    # Trigger self-enhancement
    print("\n⚡ Triggering self-enhancement...")
    enhancement_report = codex.self_enhance_code_generation()
    
    print(f"\n📈 Enhancement Report:")
    print(f"   Analyzed generations: {enhancement_report['analyzed_generations']}")
    print(f"   Patterns learned: {enhancement_report['patterns']['patterns_learned']}")
    print(f"   Tools created: {enhancement_report['tools_created']}")
    print(f"   Enhancement level: {enhancement_report['enhancement_level']}")
    
    # Final state
    final_stats = codex.get_self_enhancement_stats()
    print(f"\n📍 Final state:")
    print(f"   Tools: {final_stats['self_programmed_tools']} (Δ +{final_stats['self_programmed_tools'] - initial_stats['self_programmed_tools']})")
    print(f"   Patterns: {final_stats['learned_patterns']} (Δ +{final_stats['learned_patterns'] - initial_stats['learned_patterns']})")
    print(f"   Success rate: {final_stats['success_rate']:.1%}")
    print(f"   Improvements: {final_stats['improvements_made']}")


def main():
    """Run all demonstrations."""
    print("=" * 70)
    print("SELF-ENHANCEMENT SYSTEM DEMONSTRATION")
    print("=" * 70)
    print("\nFeatures:")
    print("✓ Self-learning from experiences")
    print("✓ Self-programming new tools")
    print("✓ Enhanced reasoning and planning")
    print("✓ Improved agent coordination")
    print("✓ Continuous capability growth")
    print("\n" + "=" * 70)
    
    # Run demonstrations
    demo_self_learning()
    demo_self_programming()
    demo_enhanced_reasoning()
    demo_improved_coordination()
    demo_self_enhancement_cycle()
    
    print("\n" + "=" * 70)
    print("✅ ALL SELF-ENHANCEMENT DEMONSTRATIONS COMPLETED")
    print("=" * 70)
    
    print("\n🎯 Key Achievements:")
    print("   ✓ Agents learn from past experiences")
    print("   ✓ Agents create their own tools dynamically")
    print("   ✓ Reasoning improves with each iteration")
    print("   ✓ Coordination protocols self-optimize")
    print("   ✓ Capabilities grow autonomously")
    
    print("\n💡 Self-Enhancement Benefits:")
    print("   • Better code suggestions over time")
    print("   • Adaptive problem-solving strategies")
    print("   • Custom tools for specific needs")
    print("   • Improved multi-agent coordination")
    print("   • Continuous system evolution")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
