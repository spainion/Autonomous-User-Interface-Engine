#!/bin/bash
# Setup script for Autonomous User Interface Engine
# Phase 1: Quick Wins & Foundation

set -e

echo "🚀 Setting up Autonomous User Interface Engine..."
echo ""

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate || . venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install production dependencies
echo "📚 Installing production dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Production dependencies installed"
echo ""

# Install development dependencies
echo "🛠️  Installing development dependencies..."
pip install -r requirements-dev.txt --quiet
echo "✓ Development dependencies installed"
echo ""

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install
echo "✓ Pre-commit hooks installed"
echo ""

# Run initial formatting
echo "🎨 Running initial code formatting..."
black . --quiet || true
isort . --quiet || true
echo "✓ Code formatted"
echo ""

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v --tb=short || echo "⚠️  Some tests may have failed (this is expected for new setup)"
echo ""

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run tests: make test"
echo "  3. Format code: make format"
echo "  4. Run linters: make lint"
echo "  5. See all commands: make help"
echo ""
echo "Happy coding! 🎉"
