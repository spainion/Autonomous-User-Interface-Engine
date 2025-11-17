"""
Rich Component Library
Generates actual, working UI components with proper HTML/CSS/JS
"""

from typing import Tuple


class RichComponentLibrary:
    """Library of rich, functional UI components"""
    
    @staticmethod
    def generate_navbar(project_name: str, primary_color: str) -> Tuple[str, str, str]:
        """Generate a functional navigation bar"""
        html = f'''<nav class="navbar">
    <div class="navbar-container">
        <div class="navbar-brand">
            <h1 class="brand-text">{project_name}</h1>
        </div>
        <ul class="navbar-menu">
            <li class="nav-item"><a href="#home" class="nav-link">Home</a></li>
            <li class="nav-item"><a href="#features" class="nav-link">Features</a></li>
            <li class="nav-item"><a href="#pricing" class="nav-link">Pricing</a></li>
            <li class="nav-item"><a href="#about" class="nav-link">About</a></li>
            <li class="nav-item"><a href="#contact" class="nav-link">Contact</a></li>
        </ul>
        <button class="navbar-toggle" aria-label="Toggle navigation">
            <span></span>
            <span></span>
            <span></span>
        </button>
    </div>
</nav>'''
        
        css = f'''
.navbar {{
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 1rem 0;
}}

.navbar-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.navbar-brand .brand-text {{
    font-size: 1.5rem;
    font-weight: 700;
    color: {primary_color};
    margin: 0;
}}

.navbar-menu {{
    display: flex;
    list-style: none;
    gap: 2rem;
    margin: 0;
    padding: 0;
}}

.nav-item {{
    display: inline;
}}

.nav-link {{
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.nav-link:hover {{
    color: {primary_color};
}}

.navbar-toggle {{
    display: none;
    flex-direction: column;
    gap: 4px;
    background: none;
    border: none;
    cursor: pointer;
}}

.navbar-toggle span {{
    width: 25px;
    height: 3px;
    background: #333;
    transition: 0.3s;
}}

@media (max-width: 768px) {{
    .navbar-menu {{
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        flex-direction: column;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: none;
    }}
    
    .navbar-menu.active {{
        display: flex;
    }}
    
    .navbar-toggle {{
        display: flex;
    }}
}}
'''
        
        js = '''
document.querySelector('.navbar-toggle').addEventListener('click', function() {
    document.querySelector('.navbar-menu').classList.toggle('active');
});
'''
        
        return html, css, js
    
    @staticmethod
    def generate_hero(project_name: str, description: str, primary_color: str) -> Tuple[str, str, str]:
        """Generate a hero section"""
        html = f'''<section class="hero">
    <div class="hero-content">
        <h1 class="hero-title">{project_name}</h1>
        <p class="hero-description">{description}</p>
        <div class="hero-actions">
            <button class="btn btn-primary">Get Started</button>
            <button class="btn btn-secondary">Learn More</button>
        </div>
    </div>
</section>'''
        
        css = f'''
.hero {{
    background: linear-gradient(135deg, {primary_color}15 0%, {primary_color}05 100%);
    padding: 6rem 1.5rem;
    text-align: center;
}}

.hero-content {{
    max-width: 800px;
    margin: 0 auto;
}}

.hero-title {{
    font-size: 3rem;
    font-weight: 800;
    color: #1a1a1a;
    margin-bottom: 1.5rem;
    line-height: 1.2;
}}

.hero-description {{
    font-size: 1.25rem;
    color: #666;
    margin-bottom: 2rem;
    line-height: 1.6;
}}

.hero-actions {{
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}}

@media (max-width: 768px) {{
    .hero-title {{
        font-size: 2rem;
    }}
    
    .hero-description {{
        font-size: 1rem;
    }}
}}
'''
        
        js = ''
        return html, css, js
    
    @staticmethod
    def generate_card(title: str, content: str, card_type: str = "basic") -> Tuple[str, str, str]:
        """Generate a card component"""
        html = f'''<div class="card">
    <div class="card-header">
        <h3 class="card-title">{title}</h3>
    </div>
    <div class="card-body">
        <p class="card-text">{content}</p>
    </div>
    <div class="card-footer">
        <button class="btn btn-sm">Learn More</button>
    </div>
</div>'''
        
        css = '''
.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.card-header {
    padding: 1.5rem;
    border-bottom: 1px solid #eee;
}

.card-title {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a1a1a;
}

.card-body {
    padding: 1.5rem;
}

.card-text {
    margin: 0;
    color: #666;
    line-height: 1.6;
}

.card-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #eee;
    background: #f9f9f9;
}
'''
        
        js = ''
        return html, css, js
    
    @staticmethod
    def generate_button(primary_color: str) -> Tuple[str, str, str]:
        """Generate button styles"""
        html = '<button class="btn btn-primary">Click Me</button>'
        
        css = f'''
.btn {{
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 500;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}}

.btn-primary {{
    background: {primary_color};
    color: white;
}}

.btn-primary:hover {{
    background: {primary_color}dd;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}}

.btn-secondary {{
    background: white;
    color: {primary_color};
    border: 2px solid {primary_color};
}}

.btn-secondary:hover {{
    background: {primary_color};
    color: white;
}}

.btn-sm {{
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
}}
'''
        
        js = '''
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function() {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
        }, 100);
    });
});
'''
        
        return html, css, js
    
    @staticmethod
    def generate_form(form_type: str, primary_color: str) -> Tuple[str, str, str]:
        """Generate a form component"""
        if form_type == "contact":
            html = '''<form class="form contact-form">
    <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" class="form-input" required>
    </div>
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" class="form-input" required>
    </div>
    <div class="form-group">
        <label for="message">Message</label>
        <textarea id="message" name="message" class="form-input" rows="4" required></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Send Message</button>
</form>'''
        elif form_type == "search":
            html = '''<form class="form search-form">
    <div class="search-wrapper">
        <input type="search" placeholder="Search..." class="search-input">
        <button type="submit" class="search-btn">
            <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
                <path d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"/>
            </svg>
        </button>
    </div>
</form>'''
        else:
            html = '<form class="form"><p>Form component</p></form>'
        
        css = f'''
.form {{
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

.form-group {{
    margin-bottom: 1.5rem;
}}

.form-group label {{
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #333;
}}

.form-input {{
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}}

.form-input:focus {{
    outline: none;
    border-color: {primary_color};
    box-shadow: 0 0 0 3px {primary_color}20;
}}

.search-wrapper {{
    display: flex;
    gap: 0.5rem;
}}

.search-input {{
    flex: 1;
    padding: 0.75rem 1rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
}}

.search-btn {{
    padding: 0.75rem 1rem;
    background: {primary_color};
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.3s ease;
}}

.search-btn:hover {{
    background: {primary_color}dd;
}}
'''
        
        js = '''
document.querySelectorAll('.form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Form submitted!');
    });
});
'''
        
        return html, css, js
    
    @staticmethod
    def generate_features_section(features: list, primary_color: str) -> Tuple[str, str, str]:
        """Generate a features section"""
        feature_items = ''.join([
            f'''<div class="feature-item">
                <div class="feature-icon">✓</div>
                <h3 class="feature-title">{feature}</h3>
                <p class="feature-description">Experience the power of {feature.lower()} in your workflow.</p>
            </div>'''
            for feature in features[:4]
        ])
        
        html = f'''<section class="features-section">
    <div class="features-container">
        <h2 class="section-title">Key Features</h2>
        <div class="features-grid">
            {feature_items}
        </div>
    </div>
</section>'''
        
        css = f'''
.features-section {{
    padding: 4rem 1.5rem;
    background: white;
}}

.features-container {{
    max-width: 1200px;
    margin: 0 auto;
}}

.section-title {{
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 3rem;
    color: #1a1a1a;
}}

.features-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}}

.feature-item {{
    text-align: center;
    padding: 2rem;
    border-radius: 8px;
    transition: transform 0.3s ease;
}}

.feature-item:hover {{
    transform: translateY(-8px);
}}

.feature-icon {{
    width: 60px;
    height: 60px;
    background: {primary_color};
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 auto 1rem;
}}

.feature-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    color: #1a1a1a;
}}

.feature-description {{
    color: #666;
    line-height: 1.6;
}}
'''
        
        js = ''
        return html, css, js
