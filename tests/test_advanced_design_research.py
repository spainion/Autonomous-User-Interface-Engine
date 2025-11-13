"""
Tests for Advanced Design Research Engine
"""

import pytest
from advanced_design_research import (
    AdvancedDesignResearchEngine,
    AdvancedDesignPattern,
    DesignTrend,
    DesignAnalysis
)


class TestAdvancedDesignResearchEngine:
    """Test suite for Advanced Design Research Engine"""
    
    @pytest.fixture
    def engine(self):
        """Create engine instance for testing"""
        return AdvancedDesignResearchEngine(use_context_engine=False)
    
    def test_initialization(self, engine):
        """Test engine initializes with patterns and trends"""
        assert len(engine.pattern_database) > 500
        assert len(engine.trend_database) >= 5
        assert len(engine.category_index) >= 10
        assert len(engine.tag_index) > 0
    
    def test_search_patterns_basic(self, engine):
        """Test basic pattern search"""
        results = engine.search_patterns("hero", limit=10)
        assert len(results) > 0
        assert all(isinstance(p, AdvancedDesignPattern) for p in results)
        assert all('hero' in p.name.lower() or 'hero' in p.subcategory.lower() 
                   for p in results)
    
    def test_search_patterns_with_category_filter(self, engine):
        """Test search with category filter"""
        results = engine.search_patterns(
            query="card",
            category="components",
            limit=20
        )
        assert all(p.category == "components" for p in results)
    
    def test_search_patterns_with_accessibility_filter(self, engine):
        """Test search with accessibility filter"""
        min_accessibility = 0.90
        results = engine.search_patterns(
            query="form",
            min_accessibility=min_accessibility,
            limit=20
        )
        assert all(p.accessibility_score >= min_accessibility for p in results)
    
    def test_search_patterns_with_performance_filter(self, engine):
        """Test search with performance filter"""
        min_performance = 0.85
        results = engine.search_patterns(
            query="button",
            min_performance=min_performance,
            limit=20
        )
        assert all(p.performance_score >= min_performance for p in results)
    
    def test_search_patterns_with_complexity_filter(self, engine):
        """Test search with complexity filter"""
        results = engine.search_patterns(
            query="dashboard",
            complexity="simple",
            limit=20
        )
        assert all(p.complexity_level == "simple" for p in results)
    
    def test_search_patterns_with_tags_filter(self, engine):
        """Test search with tags filter"""
        results = engine.search_patterns(
            query="modal",
            tags=["wcag-compliant"],
            limit=20
        )
        assert all("wcag-compliant" in p.tags for p in results)
    
    def test_search_patterns_empty_result(self, engine):
        """Test search with no matches"""
        results = engine.search_patterns(
            query="nonexistent_pattern_xyz123",
            limit=10
        )
        assert len(results) == 0
    
    def test_analyze_patterns_all(self, engine):
        """Test analyzing all patterns"""
        analysis = engine.analyze_patterns()
        
        assert isinstance(analysis, DesignAnalysis)
        assert analysis.pattern_count > 500
        assert len(analysis.categories) >= 10
        assert 0.0 <= analysis.avg_accessibility_score <= 1.0
        assert 0.0 <= analysis.avg_performance_score <= 1.0
        assert len(analysis.trending_patterns) > 0
        assert len(analysis.recommended_frameworks) > 0
        assert len(analysis.insights) > 0
    
    def test_analyze_patterns_subset(self, engine):
        """Test analyzing a subset of patterns"""
        patterns = engine.search_patterns("hero", limit=10)
        analysis = engine.analyze_patterns(patterns)
        
        assert analysis.pattern_count == len(patterns)
        assert len(analysis.categories) > 0
    
    def test_analyze_patterns_empty(self, engine):
        """Test analyzing empty pattern list"""
        analysis = engine.analyze_patterns([])
        
        assert analysis.pattern_count == 0
        assert len(analysis.categories) == 0
        assert analysis.avg_accessibility_score == 0.0
    
    def test_get_recommendations_landing_pages(self, engine):
        """Test getting recommendations for landing pages"""
        recs = engine.get_recommendations(
            project_type="landing_pages",
            target_audience="general",
            priority="balanced"
        )
        
        assert 'recommended_patterns' in recs
        assert 'design_trends' in recs
        assert 'analysis' in recs
        assert 'frameworks' in recs
        assert 'color_palettes' in recs
        
        assert len(recs['recommended_patterns']) > 0
        assert len(recs['design_trends']) > 0
        assert len(recs['frameworks']) > 0
    
    def test_get_recommendations_accessibility_priority(self, engine):
        """Test recommendations with accessibility priority"""
        recs = engine.get_recommendations(
            project_type="dashboards",
            priority="accessibility"
        )
        
        patterns = recs['recommended_patterns']
        # Check that patterns are sorted by accessibility
        scores = [p['scores']['accessibility'] for p in patterns]
        assert scores == sorted(scores, reverse=True)
    
    def test_get_recommendations_performance_priority(self, engine):
        """Test recommendations with performance priority"""
        recs = engine.get_recommendations(
            project_type="ecommerce",
            priority="performance"
        )
        
        patterns = recs['recommended_patterns']
        # Check that patterns are sorted by performance
        scores = [p['scores']['performance'] for p in patterns]
        assert scores == sorted(scores, reverse=True)
    
    def test_get_pattern_by_id(self, engine):
        """Test getting pattern by ID"""
        # Get a pattern ID from search
        results = engine.search_patterns("button", limit=1)
        if results:
            pattern_id = results[0].pattern_id
            pattern = engine.get_pattern_by_id(pattern_id)
            
            assert pattern is not None
            assert pattern.pattern_id == pattern_id
    
    def test_get_pattern_by_id_nonexistent(self, engine):
        """Test getting nonexistent pattern"""
        pattern = engine.get_pattern_by_id("nonexistent_pattern_123")
        assert pattern is None
    
    def test_get_trending_patterns(self, engine):
        """Test getting trending patterns"""
        trending = engine.get_trending_patterns(limit=10)
        
        assert len(trending) == 10
        assert all(isinstance(p, AdvancedDesignPattern) for p in trending)
        
        # Check that patterns are sorted by popularity
        scores = [p.popularity_score for p in trending]
        assert scores == sorted(scores, reverse=True)
    
    def test_get_statistics(self, engine):
        """Test getting engine statistics"""
        stats = engine.get_statistics()
        
        assert 'total_patterns' in stats
        assert 'total_categories' in stats
        assert 'total_tags' in stats
        assert 'total_trends' in stats
        assert 'total_searches' in stats
        assert 'most_used_patterns' in stats
        
        assert stats['total_patterns'] > 500
        assert stats['total_categories'] >= 10
        assert stats['total_trends'] >= 5
    
    def test_search_history_tracking(self, engine):
        """Test that search history is tracked"""
        initial_count = len(engine.search_history)
        
        engine.search_patterns("test1")
        engine.search_patterns("test2")
        engine.search_patterns("test3")
        
        assert len(engine.search_history) == initial_count + 3
    
    def test_pattern_usage_stats(self, engine):
        """Test that pattern usage is tracked"""
        # Search for patterns
        results = engine.search_patterns("hero", limit=5)
        if results:
            pattern_id = results[0].pattern_id
            initial_usage = engine.pattern_usage_stats[pattern_id]
            
            # Search again to increment usage
            engine.search_patterns("hero", limit=5)
            
            assert engine.pattern_usage_stats[pattern_id] > initial_usage
    
    def test_pattern_structure(self, engine):
        """Test that patterns have proper structure"""
        pattern = list(engine.pattern_database.values())[0]
        
        # Check required fields
        assert pattern.pattern_id
        assert pattern.name
        assert pattern.category
        assert pattern.subcategory
        assert pattern.description
        assert pattern.html_template
        assert pattern.css_template
        assert pattern.js_template
        
        # Check scores are in valid range
        assert 0.0 <= pattern.accessibility_score <= 1.0
        assert 0.0 <= pattern.performance_score <= 1.0
        assert 0.0 <= pattern.usability_score <= 1.0
        assert 0.0 <= pattern.popularity_score <= 1.0
        
        # Check complexity level
        assert pattern.complexity_level in ['simple', 'moderate', 'complex']
        
        # Check lists
        assert isinstance(pattern.tags, list)
        assert isinstance(pattern.best_practices, list)
        assert isinstance(pattern.anti_patterns, list)
        assert isinstance(pattern.use_cases, list)
        
        # Check dictionaries
        assert isinstance(pattern.framework_variants, dict)
        assert isinstance(pattern.responsive_breakpoints, dict)
    
    def test_trend_structure(self, engine):
        """Test that trends have proper structure"""
        trend = list(engine.trend_database.values())[0]
        
        assert trend.name
        assert trend.category
        assert 0.0 <= trend.popularity_score <= 1.0
        assert trend.year_introduced > 2000
        assert 0.0 <= trend.adoption_rate <= 1.0
        assert isinstance(trend.characteristics, list)
        assert isinstance(trend.examples, list)
        assert isinstance(trend.frameworks_supporting, list)
    
    def test_category_index(self, engine):
        """Test category index is properly built"""
        # Check that all categories have patterns
        for category, pattern_ids in engine.category_index.items():
            assert len(pattern_ids) > 0
            
            # Verify patterns exist
            for pattern_id in pattern_ids:
                assert pattern_id in engine.pattern_database
                pattern = engine.pattern_database[pattern_id]
                assert pattern.category == category
    
    def test_tag_index(self, engine):
        """Test tag index is properly built"""
        # Check that all tags have patterns
        for tag, pattern_ids in engine.tag_index.items():
            assert len(pattern_ids) > 0
            
            # Verify patterns exist
            for pattern_id in pattern_ids:
                assert pattern_id in engine.pattern_database
                pattern = engine.pattern_database[pattern_id]
                assert tag in pattern.tags
    
    def test_multiple_searches_performance(self, engine):
        """Test performance of multiple searches"""
        import time
        
        start = time.time()
        for i in range(100):
            engine.search_patterns(f"pattern{i % 10}", limit=10)
        elapsed = time.time() - start
        
        # Should complete 100 searches in reasonable time
        assert elapsed < 5.0  # 5 seconds for 100 searches
    
    def test_pattern_completeness(self, engine):
        """Test that all generated patterns are complete"""
        for pattern in engine.pattern_database.values():
            # HTML should contain template variables
            assert '{{' in pattern.html_template
            
            # CSS should be valid
            assert '{' in pattern.css_template
            assert '}' in pattern.css_template
            
            # JS should be valid
            assert 'function' in pattern.js_template or 'addEventListener' in pattern.js_template
            
            # Framework variants should be defined
            assert len(pattern.framework_variants) >= 4
            
            # Responsive breakpoints should be defined
            assert 'mobile' in pattern.responsive_breakpoints
            assert 'tablet' in pattern.responsive_breakpoints
            assert 'desktop' in pattern.responsive_breakpoints


class TestDesignAnalysis:
    """Test suite for DesignAnalysis"""
    
    def test_design_analysis_structure(self):
        """Test DesignAnalysis structure"""
        analysis = DesignAnalysis(
            pattern_count=100,
            categories={'landing_pages': 20, 'dashboards': 30},
            avg_accessibility_score=0.85,
            avg_performance_score=0.90,
            trending_patterns=['Pattern 1', 'Pattern 2'],
            recommended_frameworks=['Bootstrap', 'Tailwind'],
            color_palettes=[['#000', '#fff']],
            typography_suggestions=['Inter', 'Roboto'],
            layout_patterns=['Grid', 'Flexbox'],
            insights=['Insight 1', 'Insight 2']
        )
        
        assert analysis.pattern_count == 100
        assert len(analysis.categories) == 2
        assert analysis.avg_accessibility_score == 0.85
        assert len(analysis.insights) == 2


class TestAdvancedDesignPattern:
    """Test suite for AdvancedDesignPattern"""
    
    def test_pattern_creation(self):
        """Test creating an advanced design pattern"""
        pattern = AdvancedDesignPattern(
            pattern_id="test_001",
            name="Test Pattern",
            category="test",
            subcategory="test_sub",
            description="Test description",
            html_template="<div>Test</div>",
            css_template=".test { color: red; }",
            js_template="console.log('test');",
            framework_variants={'bootstrap': 'test'},
            accessibility_score=0.95,
            performance_score=0.90,
            usability_score=0.85,
            complexity_level="simple",
            tags=['test'],
            best_practices=['practice 1'],
            anti_patterns=['antipattern 1'],
            use_cases=['use case 1'],
            related_patterns=['pattern_002'],
            design_principles=['principle 1'],
            responsive_breakpoints={'mobile': '320px'},
            animation_support=True,
            interactions=['click'],
            popularity_score=0.88,
            last_updated="2025-01-01"
        )
        
        assert pattern.pattern_id == "test_001"
        assert pattern.name == "Test Pattern"
        assert pattern.complexity_level == "simple"
        assert pattern.animation_support is True


class TestDesignTrend:
    """Test suite for DesignTrend"""
    
    def test_trend_creation(self):
        """Test creating a design trend"""
        trend = DesignTrend(
            name="Test Trend",
            category="visual_style",
            popularity_score=0.92,
            year_introduced=2020,
            adoption_rate=0.75,
            characteristics=["char1", "char2"],
            examples=["example1"],
            frameworks_supporting=["framework1"]
        )
        
        assert trend.name == "Test Trend"
        assert trend.popularity_score == 0.92
        assert trend.year_introduced == 2020
        assert len(trend.characteristics) == 2
