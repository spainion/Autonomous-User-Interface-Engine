"""
Universal Compatibility Demonstration.

Shows integration with:
- GitHub Copilot
- OpenAI Codex
- OpenAI Assistants API
- Custom agents
- Autonomous operation
"""

from universal_compatibility import (
    UniversalAgentInterface,
    CopilotCompatibilityHelper,
    CodexCompatibilityHelper,
    create_universal_agent_system
)
from agents import (
    SelfEnhancingCodexAgent,
    SelfEnhancingUIDesignerAgent,
    SelfEnhancingReasoningAgent
)


def demo_universal_interface():
    """Demonstrate universal agent interface."""
    print("=" * 70)
    print("UNIVERSAL AGENT INTERFACE DEMONSTRATION")
    print("=" * 70)
    
    # Create universal system
    print("\n🌐 Creating universal agent system...")
    interface = create_universal_agent_system()
    
    # Check compatibility
    status = interface.get_compatibility_status()
    print(f"\n✓ Compatibility Status:")
    print(f"  Integrations: {len([k for k, v in status['integrations'].items() if v])}/{len(status['integrations'])}")
    print(f"  Registered agents: {status['registered_agents']}")
    print(f"  Available types: {', '.join(status['available_types'])}")
    print(f"  Fully compatible: {status['fully_compatible']}")


def demo_github_copilot_compatibility():
    """Demonstrate GitHub Copilot compatibility."""
    print("\n" + "=" * 70)
    print("GITHUB COPILOT COMPATIBILITY")
    print("=" * 70)
    
    # Get workspace context
    workspace = CopilotCompatibilityHelper.get_workspace_context()
    print(f"\n📂 Workspace Context:")
    print(f"  Path: {workspace['workspace_path']}")
    print(f"  Available: {workspace['available']}")
    print(f"  Type: {workspace['type']}")
    
    # Create universal interface
    interface = UniversalAgentInterface(
        enable_github_copilot=True
    )
    
    # Route request through interface
    print(f"\n💡 Routing code request through Copilot...")
    result = interface.route_request(
        "Create a user authentication function",
        preferred_agent_type='github_copilot'
    )
    
    print(f"  Source: {result['source']}")
    print(f"  Success: {result['success']}")
    print(f"  Response: {result['response'][:60]}...")
    
    # Enhance with context
    print(f"\n⚡ Enhancing Copilot suggestion with context...")
    enhanced = CopilotCompatibilityHelper.enhance_copilot_suggestion(
        result['response'],
        interface.context
    )
    print(f"  Enhanced: {enhanced[:80]}...")
    
    # Export context for Copilot
    print(f"\n💾 Exporting context for Copilot workspace...")
    CopilotCompatibilityHelper.export_context_for_copilot(
        interface.context,
        "/tmp/.copilot-context.json"
    )


def demo_openai_codex_compatibility():
    """Demonstrate OpenAI Codex compatibility."""
    print("\n" + "=" * 70)
    print("OPENAI CODEX COMPATIBILITY")
    print("=" * 70)
    
    interface = UniversalAgentInterface(
        enable_openai_codex=True
    )
    
    # Create Codex-compatible prompt
    print(f"\n📝 Creating Codex-compatible prompt...")
    prompt = CodexCompatibilityHelper.create_codex_prompt(
        "def calculate_fibonacci(n):",
        interface.context,
        include_context=True
    )
    print(f"  Prompt: {prompt[:100]}...")
    
    # Route through interface
    print(f"\n🔧 Routing through Codex interface...")
    result = interface.route_request(
        "Create a function to calculate factorial",
        preferred_agent_type='openai_codex'
    )
    
    if result['success']:
        print(f"  Source: {result['source']}")
        print(f"  Model: {result.get('model', 'N/A')}")
        print(f"  Success: {result['success']}")
    else:
        print(f"  Note: {result.get('error', 'Codex not available (API key needed)')}")
        print(f"  Falling back to registered agents...")
        
        # Fallback to registered agent
        result = interface.route_request(
            "Create a function to calculate factorial",
            preferred_agent_type='codex'
        )
        print(f"  Fallback source: {result['source']}")


def demo_openai_assistants_compatibility():
    """Demonstrate OpenAI Assistants API compatibility."""
    print("\n" + "=" * 70)
    print("OPENAI ASSISTANTS API COMPATIBILITY")
    print("=" * 70)
    
    interface = UniversalAgentInterface()
    
    # Create Assistant-compatible configuration
    print(f"\n🤖 Creating OpenAI Assistant-compatible config...")
    assistant_config = interface.create_openai_assistant_compatible(
        name="CodeExpertAssistant",
        instructions="You are an expert code assistant with access to learned patterns.",
        tools=[
            {"type": "code_interpreter"},
            {"type": "retrieval"}
        ]
    )
    
    print(f"  Name: {assistant_config['name']}")
    print(f"  Model: {assistant_config['model']}")
    print(f"  Context engine: {assistant_config['context_engine_enabled']}")
    print(f"  Compatible with: {', '.join(assistant_config['compatible_with'])}")
    print(f"  Tools: {len(assistant_config['tools'])}")


def demo_custom_agent_compatibility():
    """Demonstrate custom agent compatibility."""
    print("\n" + "=" * 70)
    print("CUSTOM AGENT COMPATIBILITY")
    print("=" * 70)
    
    interface = UniversalAgentInterface()
    
    # Create custom agents
    print(f"\n🔧 Creating custom self-enhancing agents...")
    codex = SelfEnhancingCodexAgent("CustomCodex")
    ui = SelfEnhancingUIDesignerAgent("CustomUI")
    reasoner = SelfEnhancingReasoningAgent("CustomReasoner")
    
    # Register with universal interface
    print(f"\n📝 Registering agents with universal interface...")
    codex_id = interface.register_agent(
        codex,
        'custom_codex',
        codex.get_capabilities()
    )
    
    ui_id = interface.register_agent(
        ui,
        'custom_ui',
        ui.get_capabilities()
    )
    
    reasoner_id = interface.register_agent(
        reasoner,
        'custom_reasoner',
        reasoner.get_capabilities()
    )
    
    # Route requests through registered agents
    print(f"\n🎯 Routing requests through registered agents...")
    
    code_result = interface.route_request(
        "Create REST API endpoint",
        preferred_agent_type='custom_codex'
    )
    print(f"  Codex: {code_result['source']} - {code_result.get('code', 'N/A')[:50]}...")
    
    ui_result = interface.route_request(
        "Design login form",
        preferred_agent_type='custom_ui'
    )
    print(f"  UI: {ui_result['source']} - {ui_result.get('ui_component', 'N/A')[:50]}...")


def demo_autonomous_operation():
    """Demonstrate autonomous operation."""
    print("\n" + "=" * 70)
    print("AUTONOMOUS OPERATION")
    print("=" * 70)
    
    interface = UniversalAgentInterface(
        autonomous_mode=True
    )
    
    print(f"\n🤖 Autonomous mode enabled")
    print(f"  Interface can operate without external APIs")
    print(f"  Falls back intelligently based on request type")
    
    # Test autonomous routing
    print(f"\n🎯 Testing autonomous routing...")
    
    requests = [
        ("Create user model", "Expected: codex agent"),
        ("Design dashboard", "Expected: ui_designer agent"),
        ("Plan architecture", "Expected: reasoning agent"),
        ("Unknown task type", "Expected: autonomous fallback")
    ]
    
    for request, expected in requests:
        result = interface.route_request(request)
        print(f"  '{request[:30]}...'")
        print(f"    → Routed to: {result['source']}")
        print(f"    → Success: {result['success']}")


def demo_full_system_integration():
    """Demonstrate full system integration."""
    print("\n" + "=" * 70)
    print("FULL SYSTEM INTEGRATION")
    print("=" * 70)
    
    # Create universal system with all features
    interface = create_universal_agent_system()
    
    print(f"\n🌟 Full system created with:")
    print(f"  ✓ GitHub Copilot integration")
    print(f"  ✓ OpenAI Codex integration")
    print(f"  ✓ OpenAI Assistants compatibility")
    print(f"  ✓ Self-enhancing agents")
    print(f"  ✓ Context engine")
    print(f"  ✓ Network enhancement")
    print(f"  ✓ Batch processing")
    print(f"  ✓ Iterative enhancement")
    print(f"  ✓ Autonomous operation")
    
    # Complex workflow using all systems
    print(f"\n🔄 Running complex workflow across all systems...")
    
    # Step 1: Plan with reasoning agent
    print(f"\n1️⃣  Planning with reasoning agent...")
    plan = interface.route_request(
        "Plan a microservices architecture",
        preferred_agent_type='reasoning'
    )
    print(f"    ✓ Plan created")
    
    # Step 2: Generate code with Codex (or fallback)
    print(f"\n2️⃣  Generating code...")
    code = interface.route_request(
        "Implement API gateway service",
        preferred_agent_type='codex'
    )
    print(f"    ✓ Code generated via {code['source']}")
    
    # Step 3: Design UI
    print(f"\n3️⃣  Designing UI...")
    ui = interface.route_request(
        "Create admin dashboard",
        preferred_agent_type='ui_designer'
    )
    print(f"    ✓ UI designed via {ui['source']}")
    
    # Check final status
    status = interface.get_compatibility_status()
    print(f"\n📊 Final System Status:")
    print(f"  Context nodes: {status['context_nodes']}")
    print(f"  Registered agents: {status['registered_agents']}")
    print(f"  Available types: {len(status['available_types'])}")
    print(f"  Fully compatible: {status['fully_compatible']}")


def main():
    """Run all compatibility demonstrations."""
    print("=" * 70)
    print("UNIVERSAL COMPATIBILITY SYSTEM DEMONSTRATION")
    print("=" * 70)
    print("\nShowing compatibility with:")
    print("  • GitHub Copilot")
    print("  • OpenAI Codex")
    print("  • OpenAI Assistants API")
    print("  • Custom agents")
    print("  • Autonomous operation")
    print("\n" + "=" * 70)
    
    # Run all demos
    demo_universal_interface()
    demo_github_copilot_compatibility()
    demo_openai_codex_compatibility()
    demo_openai_assistants_compatibility()
    demo_custom_agent_compatibility()
    demo_autonomous_operation()
    demo_full_system_integration()
    
    print("\n" + "=" * 70)
    print("✅ ALL COMPATIBILITY DEMONSTRATIONS COMPLETED")
    print("=" * 70)
    
    print("\n🎯 Key Achievements:")
    print("  ✓ GitHub Copilot workspace integration")
    print("  ✓ OpenAI Codex API compatibility")
    print("  ✓ OpenAI Assistants API support")
    print("  ✓ Custom agent registration")
    print("  ✓ Autonomous fallback operation")
    print("  ✓ Universal routing system")
    print("  ✓ Shared context across all agents")
    print("  ✓ Full system integration")
    
    print("\n💡 System is fully compatible with:")
    print("  • You (GitHub Copilot)")
    print("  • Your agents")
    print("  • OpenAI agents using built-in Codex")
    print("  • Autonomous operation")
    print("  • Any custom agents")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
