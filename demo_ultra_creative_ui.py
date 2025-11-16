"""
Demo: Ultra Creative UI Generator
Demonstrates the comprehensive UI generation system for 15+ business niches
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ultra_creative_ui_generator import (
    UltraCreativeUIGenerator,
    UIGenerationRequest,
    BusinessNiche
)


def demo_single_niche():
    """Demo: Generate UI for a single niche"""
    print("\n" + "="*70)
    print("DEMO 1: Single Niche UI Generation")
    print("="*70 + "\n")
    
    # Initialize generator
    generator = UltraCreativeUIGenerator(use_context_engine=True)
    
    # Create request for a real estate business
    request = UIGenerationRequest(
        business_niche=BusinessNiche.REAL_ESTATE,
        business_name="DreamHome Realty",
        business_description="Premium real estate platform connecting buyers with their dream homes",
        target_audience="Home buyers aged 25-55 with $300k-$1M budget",
        key_features=[
            "Advanced property search",
            "Virtual 3D tours",
            "Mortgage calculator",
            "Agent matching",
            "Market analytics"
        ],
        brand_colors={
            "primary": "#059669",
            "secondary": "#0D9488",
            "accent": "#D97706"
        },
        dark_mode=True,
        include_pwa=True,
        include_analytics=True,
        seo_optimized=True,
        accessibility_level="AAA",
        performance_target="excellent"
    )
    
    # Generate UI
    result = generator.generate_ui(request)
    
    # Save to file
    os.makedirs("demo_output", exist_ok=True)
    with open("demo_output/real_estate_demo.html", "w") as f:
        f.write(result.html)
    
    print("\n📊 Generation Results:")
    print(f"   Performance Score: {result.performance_metrics['lighthouse_score_estimate']}/100")
    print(f"   Accessibility Score: {result.accessibility_report['compliance_score']:.1f}/100")
    print(f"   SEO Score: {result.seo_report['seo_score']:.1f}/100")
    print(f"   Total Size: {result.performance_metrics['total_size_kb']:.1f} KB")
    print(f"   Estimated Load Time: {result.performance_metrics['estimated_load_time']:.2f}s")
    print(f"   Optimizations Applied: {result.generation_metadata['optimizations_applied']}")
    
    print("\n✅ Demo UI saved to: demo_output/real_estate_demo.html")


def demo_all_niches():
    """Demo: Generate UIs for all supported niches"""
    print("\n" + "="*70)
    print("DEMO 2: All Niches UI Generation")
    print("="*70 + "\n")
    
    # Initialize generator
    generator = UltraCreativeUIGenerator(use_context_engine=True)
    
    # Generate all niches
    results = generator.generate_all_niches(output_dir="generated_uis")
    
    print("\n📊 Summary Statistics:")
    print(f"   Total Niches: {len(results)}")
    
    # Calculate averages
    avg_performance = sum(r.performance_metrics['lighthouse_score_estimate'] for r in results.values()) / len(results)
    avg_accessibility = sum(r.accessibility_report['compliance_score'] for r in results.values()) / len(results)
    avg_seo = sum(r.seo_report['seo_score'] for r in results.values()) / len(results)
    avg_size = sum(r.performance_metrics['total_size_kb'] for r in results.values()) / len(results)
    
    print(f"   Average Performance Score: {avg_performance:.1f}/100")
    print(f"   Average Accessibility Score: {avg_accessibility:.1f}/100")
    print(f"   Average SEO Score: {avg_seo:.1f}/100")
    print(f"   Average Size: {avg_size:.1f} KB")
    
    print("\n✅ All UIs generated! View showcase at: generated_uis/index.html")


def demo_niche_comparison():
    """Demo: Compare different niches"""
    print("\n" + "="*70)
    print("DEMO 3: Niche Comparison")
    print("="*70 + "\n")
    
    generator = UltraCreativeUIGenerator(use_context_engine=True)
    
    # Compare specific niches
    niches_to_compare = [
        BusinessNiche.SAAS,
        BusinessNiche.FOOD_DELIVERY,
        BusinessNiche.GAMING,
        BusinessNiche.HEALTHCARE
    ]
    
    comparison_data = []
    
    for niche in niches_to_compare:
        request = generator._create_demo_request(niche)
        result = generator.generate_ui(request)
        
        comparison_data.append({
            "niche": niche.value,
            "performance": result.performance_metrics['lighthouse_score_estimate'],
            "accessibility": result.accessibility_report['compliance_score'],
            "seo": result.seo_report['seo_score'],
            "size_kb": result.performance_metrics['total_size_kb']
        })
    
    # Print comparison table
    print("\n📊 Niche Comparison:")
    print(f"{'Niche':<20} {'Performance':>12} {'Accessibility':>15} {'SEO':>8} {'Size (KB)':>12}")
    print("-" * 70)
    
    for data in comparison_data:
        print(f"{data['niche']:<20} {data['performance']:>12} {data['accessibility']:>15.1f} {data['seo']:>8.1f} {data['size_kb']:>12.1f}")
    
    print("\n✅ Comparison complete!")


def demo_context_engine_learning():
    """Demo: Context engine learning capabilities"""
    print("\n" + "="*70)
    print("DEMO 4: Context Engine Learning")
    print("="*70 + "\n")
    
    try:
        from agent_init import init_agent_system
        
        # Initialize with context engine
        generator = UltraCreativeUIGenerator(use_context_engine=True)
        
        if generator.context_engine:
            print("✅ Context Engine Active")
            print("   - Self-learning enabled")
            print("   - FAISS vector search active")
            print("   - Performance caching enabled")
            
            # Generate a few UIs to populate learning
            print("\n📚 Generating UIs to populate learning database...")
            
            niches = [BusinessNiche.SAAS, BusinessNiche.REAL_ESTATE, BusinessNiche.FOOD_DELIVERY]
            for niche in niches:
                request = generator._create_demo_request(niche)
                result = generator.generate_ui(request)
                print(f"   ✓ Generated and stored learning for {niche.value}")
            
            print("\n✅ Context engine now has learned patterns for better future generations!")
        else:
            print("⚠️  Context engine not available")
    
    except Exception as e:
        print(f"⚠️  Context engine demo failed: {e}")


def demo_performance_analysis():
    """Demo: Analyze performance optimizations"""
    print("\n" + "="*70)
    print("DEMO 5: Performance Optimization Analysis")
    print("="*70 + "\n")
    
    generator = UltraCreativeUIGenerator(use_context_engine=False)
    
    # Generate UI with all optimizations
    request = generator._create_demo_request(BusinessNiche.FINTECH)
    result = generator.generate_ui(request)
    
    metrics = result.performance_metrics
    
    print("📊 Performance Breakdown:")
    print(f"   HTML Size: {metrics['html_size_kb']:.2f} KB")
    print(f"   CSS Size: {metrics['css_size_kb']:.2f} KB")
    print(f"   JavaScript Size: {metrics['js_size_kb']:.2f} KB")
    print(f"   Total Size: {metrics['total_size_kb']:.2f} KB")
    print(f"   Estimated Load Time: {metrics['estimated_load_time']:.2f}s")
    print(f"   Lazy-loadable Elements: {metrics['lazy_loadable_elements']}")
    print(f"   Code Split Points: {metrics['code_split_points']}")
    print(f"   Lighthouse Score Estimate: {metrics['lighthouse_score_estimate']}/100")
    
    print("\n🎯 Optimizations Applied:")
    accessibility_features = result.accessibility_report['features_implemented']
    for feature in accessibility_features:
        print(f"   ✓ {feature}")
    
    print("\n📈 SEO Features:")
    seo_features = result.seo_report['features_implemented']
    for feature in seo_features:
        print(f"   ✓ {feature}")


def main():
    """Run all demos"""
    print("\n" + "🎨" * 35)
    print("ULTRA CREATIVE UI GENERATOR - COMPREHENSIVE DEMO")
    print("🎨" * 35)
    
    demos = [
        ("Single Niche Generation", demo_single_niche),
        ("All Niches Generation", demo_all_niches),
        ("Niche Comparison", demo_niche_comparison),
        ("Context Engine Learning", demo_context_engine_learning),
        ("Performance Analysis", demo_performance_analysis)
    ]
    
    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  {len(demos) + 1}. Run All Demos")
    
    try:
        choice = input("\nSelect demo (1-6): ").strip()
        
        if choice == str(len(demos) + 1):
            # Run all demos
            for name, demo_func in demos:
                demo_func()
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # Run selected demo
            demos[int(choice) - 1][1]()
        else:
            print("Invalid selection. Running demo 1 by default.")
            demo_single_niche()
    
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
