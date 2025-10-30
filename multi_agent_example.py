"""
Multi-Agent Collaboration Example.

Demonstrates how multiple agents use the shared Context Engine to:
- Share information
- Build on each other's work
- Maintain collective memory
- Collaborate on complex tasks
"""

from agents import CodexAgent, UIDesignerAgent, ReasoningAgent, BaseAgent


def main():
    print("=" * 70)
    print("Multi-Agent Collaboration with Shared Context Engine")
    print("=" * 70)
    
    # Create agents - they all share the same context
    print("\n🤖 Initializing Agents...")
    reasoning_agent = ReasoningAgent("PlannerBot")
    codex_agent = CodexAgent("CodeBot")
    ui_agent = UIDesignerAgent("DesignBot")
    
    print(f"✓ {reasoning_agent.agent_name} initialized")
    print(f"✓ {codex_agent.agent_name} initialized")
    print(f"✓ {ui_agent.agent_name} initialized")
    
    # Establish collaborations
    print("\n🤝 Establishing Collaborations...")
    reasoning_agent.collaborate_with("CodeBot")
    reasoning_agent.collaborate_with("DesignBot")
    codex_agent.collaborate_with("DesignBot")
    
    print(f"✓ {reasoning_agent.agent_name} collaborates with: {reasoning_agent.get_collaborators()}")
    print(f"✓ {codex_agent.agent_name} collaborates with: {codex_agent.get_collaborators()}")
    print(f"✓ {ui_agent.agent_name} collaborates with: {ui_agent.get_collaborators()}")
    
    # Scenario: Build a user authentication system
    print("\n" + "=" * 70)
    print("Task: Build a User Authentication System")
    print("=" * 70)
    
    # Step 1: Reasoning agent plans the task
    print("\n📋 Step 1: Planning (ReasoningAgent)")
    print("-" * 70)
    plan_result = reasoning_agent.process_request(
        "Create a plan for building a user authentication system",
        complexity="medium",
        domain="software_engineering"
    )
    print(f"✓ Plan created: {plan_result['reasoning']['plan']}")
    
    # Share plan with other agents
    reasoning_agent.share_with_agent("CodeBot", plan_result['reasoning'], "task_plan")
    reasoning_agent.share_with_agent("DesignBot", plan_result['reasoning'], "task_plan")
    print(f"✓ Plan shared with CodeBot and DesignBot")
    
    # Step 2: Codex agent generates backend code
    print("\n💻 Step 2: Code Generation (CodexAgent)")
    print("-" * 70)
    code_result = codex_agent.process_request(
        "Generate user authentication backend API",
        language="python"
    )
    print(f"✓ Code generated: {code_result['code'][:60]}...")
    print(f"✓ Used {code_result['similar_patterns']} similar patterns from context")
    
    # Share code with UI designer
    codex_agent.share_with_agent("DesignBot", code_result['code'], "backend_code")
    print(f"✓ Code shared with DesignBot")
    
    # Step 3: UI designer creates frontend
    print("\n🎨 Step 3: UI Design (UIDesignerAgent)")
    print("-" * 70)
    ui_result = ui_agent.process_request(
        "Create login and signup UI components",
        framework="react",
        style="modern"
    )
    print(f"✓ UI component created: {ui_result['ui_component'][:60]}...")
    print(f"✓ Used {ui_result['similar_designs']} similar designs from context")
    
    # Share UI with code agent
    ui_agent.share_with_agent("CodeBot", ui_result['ui_component'], "frontend_ui")
    print(f"✓ UI shared with CodeBot")
    
    # Show context statistics for each agent
    print("\n" + "=" * 70)
    print("Agent Context Statistics")
    print("=" * 70)
    
    for agent in [reasoning_agent, codex_agent, ui_agent]:
        stats = agent.get_context_stats()
        print(f"\n{agent.agent_name} ({agent.agent_type}):")
        print(f"  Items Created: {stats['items_created']}")
        print(f"  Total Context Nodes: {stats['total_context_nodes']}")
        print(f"  Total Relationships: {stats['total_relationships']}")
        print(f"  Collaborators: {stats['collaborators']}")
    
    # Demonstrate shared context access
    print("\n" + "=" * 70)
    print("Shared Context Verification")
    print("=" * 70)
    
    shared_context = BaseAgent.get_shared_context()
    if shared_context:
        all_stats = shared_context.get_statistics()
        print(f"\n✓ All agents share the same context engine")
        print(f"  Total Nodes: {all_stats['n_nodes']}")
        print(f"  Total Edges: {all_stats['n_edges']}")
        print(f"  Node Types: {all_stats['node_types']}")
        print(f"  Edge Types: {all_stats['edge_types']}")
    
    # Show agent history
    print("\n" + "=" * 70)
    print("Agent Interaction History")
    print("=" * 70)
    
    for agent in [reasoning_agent, codex_agent, ui_agent]:
        history = agent.get_agent_history()
        print(f"\n{agent.agent_name} created {len(history)} items:")
        for item in history[:3]:  # Show first 3
            print(f"  • [{item.node_type}] {str(item.content)[:50]}...")
    
    # Store patterns for future reuse
    print("\n" + "=" * 70)
    print("Storing Patterns for Future Reuse")
    print("=" * 70)
    
    codex_agent.store_code_pattern(
        "authentication_api",
        "def authenticate(username, password): ...",
        "Standard authentication API pattern"
    )
    print(f"✓ CodexAgent stored 'authentication_api' pattern")
    
    ui_agent.store_design_pattern(
        "login_form",
        "<form><input type='text'/><input type='password'/></form>",
        "Standard login form pattern"
    )
    print(f"✓ UIDesignerAgent stored 'login_form' pattern")
    
    reasoning_agent.store_reasoning_pattern(
        "security_planning",
        {"steps": ["Identify risks", "Design mitigation", "Test security"]},
        "Security planning reasoning pattern"
    )
    print(f"✓ ReasoningAgent stored 'security_planning' pattern")
    
    # Final stats
    final_stats = shared_context.get_statistics()
    print("\n" + "=" * 70)
    print("Final Context State")
    print("=" * 70)
    print(f"\n✓ Total Knowledge Nodes: {final_stats['n_nodes']}")
    print(f"✓ Total Relationships: {final_stats['n_edges']}")
    print(f"✓ Graph Density: {final_stats['graph_density']:.3f}")
    print(f"\nNode Type Distribution:")
    for node_type, count in final_stats['node_types'].items():
        print(f"  • {node_type}: {count}")
    print(f"\nEdge Type Distribution:")
    for edge_type, count in final_stats['edge_types'].items():
        print(f"  • {edge_type}: {count}")
    
    print("\n" + "=" * 70)
    print("✓ Multi-Agent Collaboration Demo Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  • All agents share the same Context Engine")
    print("  • Agents can recall each other's work")
    print("  • Information flows seamlessly between agents")
    print("  • Patterns are stored for future reuse")
    print("  • Context grows richer with each interaction")
    print("=" * 70)


if __name__ == "__main__":
    main()
