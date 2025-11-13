"""Quick test for Round 2 systems"""

def test_premium_themes():
    from premium_theme_system import PremiumThemeSystem
    system = PremiumThemeSystem()
    assert len(system.list_themes()) == 15
    theme = system.get_theme("modern_blue")
    assert theme is not None
    assert theme.name == "Modern Blue"
    css = system.export_theme_css("dark_pro")
    assert "color-primary" in css
    print("✅ Premium Themes: PASS")

def test_gradients():
    from advanced_gradient_system import AdvancedGradientSystem
    gradients = AdvancedGradientSystem()
    assert len(gradients.list_gradients()) >= 18
    fire = gradients.get_gradient("fire_blaze")
    assert fire is not None
    css = fire.to_css()
    assert "linear-gradient" in css
    print("✅ Gradients: PASS")

def test_animations():
    from advanced_animation_library import AdvancedAnimationLibrary
    animations = AdvancedAnimationLibrary()
    assert len(animations.list_animations()) >= 25
    fade = animations.get_animation("fade_in")
    assert fade is not None
    css = fade.to_complete_css("fade-in")
    assert "@keyframes" in css
    print("✅ Animations: PASS")

if __name__ == "__main__":
    test_premium_themes()
    test_gradients()
    test_animations()
    print("\n🎉 All Round 2 Systems: PASS")
