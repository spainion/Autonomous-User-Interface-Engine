# Contributing to Autonomous User Interface Engine

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## 🚀 Quick Start

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Autonomous-User-Interface-Engine.git
cd Autonomous-User-Interface-Engine
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

## 📝 Development Guidelines

### Code Style

We follow these coding standards:

- **Python**: PEP 8 with Black formatting
- **Line Length**: 120 characters
- **Import Sorting**: isort with Black profile
- **Type Hints**: Encouraged for public APIs

#### Running Code Formatters

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Run all formatters
pre-commit run --all-files
```

### Linting

We use multiple linters to ensure code quality:

```bash
# Run Flake8
flake8 .

# Run Pylint
pylint **/*.py

# Run mypy for type checking
mypy .

# Run all checks
pre-commit run --all-files
```

### Testing

All code changes should include tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run tests in watch mode (requires pytest-watch)
ptw
```

**Test Coverage Requirements:**
- New features: Minimum 80% coverage
- Bug fixes: Add regression test
- Critical paths: 90%+ coverage

### Documentation

- **Docstrings**: Use Google or NumPy style
- **README**: Update for new features
- **API Docs**: Auto-generated with Sphinx
- **Examples**: Add to `examples/` directory

#### Docstring Example

```python
def generate_ui(prompt: str, theme: str = "modern") -> dict:
    """Generate a user interface from a text prompt.
    
    Args:
        prompt: Natural language description of desired UI
        theme: Theme name (default: "modern")
        
    Returns:
        Dictionary containing HTML, CSS, and JavaScript code
        
    Raises:
        ValueError: If prompt is empty or theme is invalid
        
    Example:
        >>> result = generate_ui("Create a login form")
        >>> print(result['html'])
    """
    pass
```

## 🔄 Contribution Workflow

### 1. Make Changes

```bash
# Make your changes
# Run tests frequently
pytest tests/

# Run linters
pre-commit run --all-files
```

### 2. Commit Changes

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Feature
git commit -m "feat: add advanced gradient system"

# Bug fix
git commit -m "fix: resolve cache invalidation issue"

# Documentation
git commit -m "docs: update API reference"

# Performance
git commit -m "perf: optimize FAISS indexing by 50%"

# Refactor
git commit -m "refactor: simplify context engine API"

# Test
git commit -m "test: add integration tests for agents"
```

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance tasks

### 3. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Fill out the PR template
```

## 📋 Pull Request Guidelines

### PR Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines (Black, isort)
- [ ] All tests pass (`pytest`)
- [ ] New tests added for new features
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow Conventional Commits
- [ ] PR description clearly explains changes
- [ ] No merge conflicts with main branch

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested the changes

## Checklist
- [ ] Tests pass
- [ ] Linters pass
- [ ] Documentation updated
```

### Code Review Process

1. **Automated Checks**: CI pipeline runs automatically
2. **Peer Review**: At least one approval required
3. **Address Feedback**: Make requested changes
4. **Merge**: Maintainer will merge approved PRs

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues
2. Try to reproduce with latest version
3. Gather relevant information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. ...
2. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.5]
- Version: [e.g., 0.3.0]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives**
Other solutions considered

**Additional Context**
Any other relevant information
```

## 🏗️ Project Structure

```
Autonomous-User-Interface-Engine/
├── context_engine/       # Core context management
├── agents/              # Agent implementations
├── integrations/        # External integrations
├── ui_components/       # UI generation
├── tests/              # Test suite
├── docs/               # Documentation
├── examples/           # Usage examples
└── .github/            # CI/CD workflows
```

## 🧪 Testing Guidelines

### Test Organization

```
tests/
├── unit/              # Unit tests
├── integration/       # Integration tests
├── e2e/              # End-to-end tests
└── fixtures/         # Test data
```

### Writing Tests

```python
import pytest
from context_engine import ContextEngine

def test_context_engine_initialization():
    """Test that context engine initializes correctly."""
    engine = ContextEngine()
    assert engine is not None
    assert engine.node_count() == 0

@pytest.fixture
def sample_engine():
    """Fixture for reusable engine instance."""
    engine = ContextEngine()
    engine.add_node("test", "Test node")
    return engine

def test_add_node(sample_engine):
    """Test adding nodes to engine."""
    sample_engine.add_node("node2", "Second node")
    assert sample_engine.node_count() == 2
```

## 🔒 Security

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security concerns to the maintainers
2. Include details of the vulnerability
3. Suggest a fix if possible

### Security Best Practices

- Never commit API keys or secrets
- Use `.env` files for configuration
- Validate all user inputs
- Follow OWASP guidelines

## 📚 Additional Resources

- [Documentation](README.md)
- [Architecture Guide](ARCHITECTURE.md)
- [Upgrade Plan](COMPREHENSIVE_UPGRADE_PLAN.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## 💬 Community

- **Issues**: [GitHub Issues](https://github.com/spainion/Autonomous-User-Interface-Engine/issues)
- **Discussions**: [GitHub Discussions](https://github.com/spainion/Autonomous-User-Interface-Engine/discussions)
- **Pull Requests**: [GitHub PRs](https://github.com/spainion/Autonomous-User-Interface-Engine/pulls)

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

Thank you for contributing to Autonomous User Interface Engine!
