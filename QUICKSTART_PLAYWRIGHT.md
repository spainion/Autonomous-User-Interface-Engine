# Quick Start: Playwright UI Preview & AI Enhancement

Get started with the Playwright UI preview and AI enhancement system in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Install Python packages
pip install playwright requests python-dotenv

# Install Playwright browsers
playwright install chromium
```

### 2. Generate UIs and View Gallery

```bash
# Generate 8 beautiful UIs from plain language
python playwright_ui_previewer.py

# Start local server
python -m http.server 8080 --directory playwright_previews

# Open in browser: http://localhost:8080/index.html
```

That's it! You now have:
- ✅ 8 generated UIs from plain language descriptions
- ✅ Full-page screenshots of each UI
- ✅ Interactive gallery to browse and preview
- ✅ Quality metrics for each UI

## 🤖 AI Enhancement (Optional)

To use AI models to analyze and enhance your UIs:

### 1. Get OpenRouter API Key

1. Sign up at https://openrouter.ai/
2. Add credit to your account ($5-10 recommended)
3. Copy your API key

### 2. Configure API Key

```bash
# Option 1: Environment variable
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Option 2: .env file
cp .env.template .env
# Edit .env and add your OPENROUTER_API_KEY
```

### 3. Run AI Enhancement

```bash
# Analyze UIs with 4 AI models (GPT-4, Claude-3, Gemini Pro, GPT-3.5)
python ai_ui_enhancer.py

# Or try demo mode first (no API key needed)
python ai_ui_enhancer_demo.py
```

This will:
- ✅ Analyze UIs with multiple AI models
- ✅ Generate enhancement recommendations
- ✅ Create implementation roadmap
- ✅ Produce interactive HTML report

## 📊 What You Get

### Playwright UI Previewer Output

```
playwright_previews/
├── index.html              # 👈 Open this in your browser!
├── manifest.json           # Metadata
├── generated_html/         # 8 complete UIs
│   ├── cloudflow_pro.html
│   ├── techmart.html
│   ├── dataviz_pro.html
│   └── ... (5 more)
└── screenshots/            # Full-page screenshots
    ├── cloudflow_pro.png
    └── ... (7 more)
```

### AI Enhancement Output (with API key)

```
ai_enhanced/
├── enhancement_results.html  # 👈 Open to see AI analysis!
└── enhancements.json        # Raw data
```

## 🎨 Generated UIs

The system generates 8 diverse UIs:

1. **CloudFlow Pro** - Modern SaaS landing page (Blue)
2. **TechMart** - Minimal e-commerce store (Green)
3. **DataViz Pro** - Bold analytics dashboard (Purple)
4. **CreativeStudio** - Modern portfolio website (Orange)
5. **DeliciousEats** - Classic restaurant site (Red)
6. **WealthTracker** - Modern fintech app (Green)
7. **LearnHub** - Minimal education platform (Orange)
8. **HealthConnect** - Modern healthcare portal (Cyan)

## 💡 Example Plain Language Inputs

The system understands natural language like:

```
"Create a modern SaaS landing page for a cloud storage product with a professional blue theme"
→ Generates CloudFlow Pro

"Build a minimal e-commerce store for tech products with a clean green design"
→ Generates TechMart

"Design a bold analytics dashboard with data visualization in purple"
→ Generates DataViz Pro
```

## 🎯 AI Enhancement Features

When you run the AI enhancer, you get:

### 1. Structure Analysis (GPT-4)
- Architecture assessment
- Missing elements identification
- Improvement priorities
- Rating: X/10

### 2. Creative Enhancements (Claude-3)
- Visual design ideas
- Interactive elements
- Micro-interactions
- Modern trends

### 3. Practical Improvements (Gemini Pro)
- Usability fixes
- Accessibility enhancements
- Performance optimizations
- SEO recommendations

### 4. Menu Enhancements (GPT-3.5)
- Navigation structure
- User journey optimization
- Call-to-action placement
- Menu item recommendations

### 5. Synthesis (GPT-4)
- Top 5 priority improvements
- Quick wins
- Long-term strategy
- Implementation roadmap

## 🔧 Customize

### Add Your Own UI Request

Edit `playwright_ui_previewer.py`:

```python
PLAIN_LANGUAGE_REQUESTS.append({
    "plain_language": "Create a modern blog about artificial intelligence",
    "request": CompleteUIRequest(
        project_name="AI Blog",
        project_type="landing_page",
        style="modern",
        primary_color="#8b5cf6",
        target_audience="tech enthusiasts",
        key_features=["Articles", "Categories", "Search"],
        framework="custom",
        responsive=True,
        accessibility=True,
        animations=True
    )
})
```

### Change AI Models

Edit `ai_ui_enhancer.py`:

```python
self.models = {
    'reasoning': 'openai/gpt-4-turbo-preview',
    'creativity': 'anthropic/claude-3-opus',
    'practical': 'google/gemini-pro',
    'fast': 'openai/gpt-3.5-turbo'
}
```

Browse available models: https://openrouter.ai/models

## 📚 Full Documentation

For detailed information, see:
- `PLAYWRIGHT_PREVIEW_GUIDE.md` - Complete guide
- `README.md` - Project overview
- `.env.template` - Environment configuration

## ❓ Troubleshooting

### Browser not found
```bash
playwright install chromium
```

### Port already in use
```bash
python -m http.server 8081 --directory playwright_previews
```

### API key not working
```bash
# Check if set
echo $OPENROUTER_API_KEY

# Try demo mode instead
python ai_ui_enhancer_demo.py
```

## 💰 Costs

### Free
- UI generation
- Screenshot capture
- Gallery creation
- Demo mode

### Paid (OpenRouter API)
- AI enhancement: ~$0.10-0.50 per UI
- Cost depends on models used
- GPT-4 most expensive, GPT-3.5 cheapest

## 🎉 That's It!

You're now ready to:
1. Generate beautiful UIs from plain language ✅
2. Capture screenshots with Playwright ✅
3. Browse interactive gallery ✅
4. Enhance with AI (optional) ✅

Happy building! 🚀
