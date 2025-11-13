# Intelligent LLM Orchestration System

## Overview

The Intelligent LLM Orchestrator provides advanced orchestration of OpenRouter API models with intelligent prompting strategies, dynamic model selection, and multi-model consensus capabilities.

## Key Features

### 1. **Intelligent Model Selection**
- Task-aware model routing
- Complexity-based selection
- Budget-conscious optimization
- Performance tracking

### 2. **Advanced Prompting Strategies**
- **Zero-Shot**: Direct prompting without examples
- **Few-Shot**: Learning from provided examples
- **Chain-of-Thought (CoT)**: Step-by-step reasoning
- **Tree-of-Thought (ToT)**: Exploring multiple solution paths
- **ReAct**: Combining reasoning with actions
- **Self-Consistency**: Multiple reasoning paths for validation
- **Instruction Following**: Detailed, structured instructions

### 3. **Multi-Model Orchestration**
- Parallel execution across multiple models
- Consensus building
- Result synthesis
- Confidence scoring

### 4. **Performance Optimization**
- Response caching with SHA-256 keys
- Cost tracking per model
- Latency monitoring
- Cache hit rate optimization

### 5. **Model Support**
- **OpenAI**: GPT-4 Turbo, GPT-4, GPT-3.5 Turbo
- **Anthropic**: Claude 3 Opus, Claude 3 Sonnet
- **Google**: Gemini Pro
- **Mistral**: Mixtral 8x7B
- **Meta**: Llama 3 70B

## Quick Start

### Basic Usage

```python
from intelligent_llm_orchestrator import IntelligentLLMOrchestrator, TaskType

# Initialize orchestrator
orchestrator = IntelligentLLMOrchestrator(api_key="your_openrouter_key")

# Select best model for task
model = orchestrator.select_best_model(
    task_type=TaskType.CODE_GENERATION,
    complexity='high',
    budget=0.02  # Max cost per 1K tokens
)

print(f"Selected model: {orchestrator.models[model].display_name}")
```

### Building Intelligent Prompts

```python
# Build a Chain-of-Thought prompt for code generation
system_prompt, user_prompt = orchestrator.build_prompt(
    template_id='code_generation_cot',
    variables={
        'task_description': 'Create a binary search tree in Python'
    }
)

# Execute request
response = orchestrator.execute_llm_request(
    model_key='gpt-4-turbo',
    system_prompt=system_prompt,
    user_prompt=user_prompt
)

print(f"Generated code:\n{response.content}")
print(f"Cost: ${response.cost:.4f}")
print(f"Tokens: {response.tokens_used}")
```

### Multi-Model Orchestration

```python
# Use multiple models for consensus
result = orchestrator.orchestrate_with_consensus(
    task_type=TaskType.REASONING,
    template_id='reasoning_tot',
    variables={'problem': 'How to optimize database queries?'},
    num_models=3,
    temperature=0.7
)

print(f"Primary response: {result.primary_response.content[:200]}...")
print(f"Synthesized result: {result.synthesized_result[:200]}...")
print(f"Confidence: {result.confidence:.0%}")
print(f"Total cost: ${result.total_cost:.4f}")
```

## Prompt Templates

### 1. Code Generation (Chain-of-Thought)

**Template ID**: `code_generation_cot`  
**Strategy**: Chain-of-Thought  
**Best For**: Complex code generation tasks

```python
variables = {
    'task_description': 'Your task description here'
}
```

**System Prompt**: Guides the model to think step-by-step through requirements, planning, edge cases, and implementation.

### 2. UI Design (Instruction Following)

**Template ID**: `ui_design_detailed`  
**Strategy**: Instruction Following  
**Best For**: Creating comprehensive UI designs

```python
variables = {
    'requirements': 'Create a dashboard interface',
    'framework': 'bootstrap',
    'style': 'modern'
}
```

**Output Includes**:
- Layout structure
- Component breakdown
- Visual design
- Interactions
- Accessibility features
- Responsive design
- Implementation code

### 3. Code Analysis (Chain-of-Thought)

**Template ID**: `code_analysis_detailed`  
**Strategy**: Chain-of-Thought  
**Best For**: Thorough code reviews

```python
variables = {
    'language': 'python',
    'code': 'Your code here'
}
```

**Analysis Covers**:
- Functionality and correctness
- Code quality
- Performance
- Security
- Best practices
- Specific improvements

### 4. Reasoning (Tree-of-Thought)

**Template ID**: `reasoning_tot`  
**Strategy**: Tree-of-Thought  
**Best For**: Complex problem solving

```python
variables = {
    'problem': 'Your problem statement'
}
```

**Process**:
1. Understanding the problem
2. Generating multiple approaches
3. Evaluating each approach
4. Selecting best solution
5. Implementation steps

### 5. Classification (Few-Shot)

**Template ID**: `classification_few_shot`  
**Strategy**: Few-Shot Learning  
**Best For**: Classification tasks

```python
variables = {
    'examples': 'Input: X\nOutput: Y\n...',
    'input': 'Item to classify'
}
```

**Includes**: Pre-loaded examples for better accuracy

### 6. Problem Solving (ReAct)

**Template ID**: `problem_solving_react`  
**Strategy**: ReAct (Reason + Act)  
**Best For**: Interactive problem solving

```python
variables = {
    'question': 'Your question'
}
```

**Format**:
- Thought → Action → Observation → (repeat) → Answer

## Model Selection Algorithm

### Selection Criteria

1. **Task Compatibility**: Models with strength in the task type
2. **Complexity Level**:
   - **Low**: Cheapest suitable model
   - **Medium**: Balance of cost and capability
   - **High**: Most capable model
3. **Budget Constraint**: Filter by max cost per 1K tokens
4. **Fallback**: GPT-4 Turbo for unknown tasks

### Example Selection Results

```python
# Code Generation - High Complexity
model = orchestrator.select_best_model(
    TaskType.CODE_GENERATION, 
    complexity='high'
)
# Result: GPT-4 Turbo (most capable)

# Translation - Low Complexity
model = orchestrator.select_best_model(
    TaskType.TRANSLATION,
    complexity='low'
)
# Result: GPT-3.5 Turbo (cost-effective)

# With Budget Constraint
model = orchestrator.select_best_model(
    TaskType.CODE_GENERATION,
    complexity='high',
    budget=0.005  # Max $0.005 per 1K tokens
)
# Result: Mixtral 8x7B (within budget)
```

## Multi-Model Consensus

### How It Works

1. **Model Selection**: Choose multiple models suited for the task
2. **Parallel Execution**: Send requests to all models
3. **Response Collection**: Gather all responses
4. **Synthesis**: Combine insights based on task type
5. **Confidence Scoring**: Calculate agreement level

### Synthesis Strategies

#### Code Generation
```python
# Selects the longest/most complete response
# Ensures comprehensive implementation
```

#### Reasoning
```python
# Combines perspectives from all models
# Creates multi-viewpoint analysis
```

#### Default
```python
# Returns primary (first/best) response
# Falls back when synthesis unclear
```

### Confidence Calculation

```python
# Based on response similarity
# Lower variance = higher confidence
# Range: 0.5 (low) to 0.95 (high)
confidence = 1.0 - (variance / avg_length²)
```

## Performance Optimization

### Caching System

```python
# Automatic caching of responses
cache_key = SHA256(model + messages + temperature)

# Cache hits avoid API calls
if cache_key in cache:
    return cached_response  # Instant response
```

**Benefits**:
- Instant response for repeated queries
- Zero API cost on cache hits
- Reduced latency

### Cost Tracking

```python
# Per-request cost calculation
cost = (tokens_used / 1000) * model.cost_per_1k_tokens

# Metrics tracking
metrics = orchestrator.get_metrics()
# Returns:
# - total_requests
# - cache_hits
# - cache_hit_rate
# - total_cost
# - avg_cost_per_request
# - model_usage (count per model)
```

### Model Costs (per 1K tokens)

| Model | Cost | Best For |
|-------|------|----------|
| GPT-4 Turbo | $0.010 | Complex tasks |
| Claude 3 Opus | $0.015 | Creative work |
| GPT-4 | $0.030 | High-quality output |
| Claude 3 Sonnet | $0.003 | Balanced tasks |
| GPT-3.5 Turbo | $0.0015 | Simple tasks |
| Gemini Pro | $0.00025 | Budget-friendly |
| Mixtral 8x7B | $0.00027 | Open source |
| Llama 3 70B | $0.00059 | Open source |

## Integration with Enhanced NLP

### Automatic Integration

```python
from enhanced_nlp_system import EnhancedNLPSystem

# Orchestrator automatically initialized
nlp = EnhancedNLPSystem(
    context_engine=engine,
    use_orchestrator=True  # Enable orchestration
)

# Use orchestrated interpretation
interpretation = nlp.interpret_with_orchestration(
    text="Create a dashboard with charts and tables",
    use_consensus=True  # Use multi-model consensus
)
```

### Benefits of Integration

1. **Intelligent Model Selection**: Automatically chooses best model for detected intent
2. **Optimized Prompts**: Uses appropriate template for task type
3. **Enhanced Results**: Better accuracy through specialized prompts
4. **Cost Efficiency**: Balances quality with cost

## Advanced Usage

### Custom Prompt Templates

```python
from intelligent_llm_orchestrator import PromptTemplate, PromptStrategy, TaskType

# Create custom template
custom_template = PromptTemplate(
    template_id='custom_analysis',
    task_type=TaskType.DATA_EXTRACTION,
    strategy=PromptStrategy.CHAIN_OF_THOUGHT,
    system_prompt="You are a data extraction expert...",
    user_prompt_template="""Data: {data}
    
Extract: {fields}
    
Think step by step...""",
    variables=['data', 'fields']
)

# Register template
orchestrator.prompt_templates['custom_analysis'] = custom_template

# Use it
system, user = orchestrator.build_prompt(
    'custom_analysis',
    {'data': 'sample data', 'fields': 'name, email, phone'}
)
```

### Custom Model Configuration

```python
from intelligent_llm_orchestrator import ModelConfig, TaskType

# Add custom model
orchestrator.models['custom-model'] = ModelConfig(
    model_id='provider/model-name',
    display_name='Custom Model',
    provider='CustomProvider',
    strengths=[TaskType.CODE_GENERATION],
    cost_per_1k_tokens=0.001,
    max_tokens=4096,
    context_window=8192,
    best_temperature=0.7
)
```

### Fallback Strategies

```python
def execute_with_fallback(orchestrator, prompt_data):
    """Execute with automatic fallback"""
    models = ['gpt-4-turbo', 'claude-3-opus', 'gpt-3.5-turbo']
    
    for model in models:
        try:
            response = orchestrator.execute_llm_request(
                model_key=model,
                **prompt_data
            )
            return response
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
    
    raise Exception("All models failed")
```

## Best Practices

### 1. Model Selection

```python
# ✅ Good: Match task to model strengths
model = orchestrator.select_best_model(
    TaskType.CODE_GENERATION,
    complexity='high'
)

# ❌ Bad: Using expensive model for simple tasks
model = 'gpt-4'  # Overpaying for simple translation
```

### 2. Prompt Engineering

```python
# ✅ Good: Use appropriate strategy
template_id = 'code_generation_cot'  # CoT for complex code

# ❌ Bad: Generic prompting
user_prompt = "Write code for X"  # No structure
```

### 3. Caching

```python
# ✅ Good: Enable caching for repeated queries
orchestrator = IntelligentLLMOrchestrator(cache_enabled=True)

# ❌ Bad: Disabling cache unnecessarily
orchestrator = IntelligentLLMOrchestrator(cache_enabled=False)
```

### 4. Multi-Model Usage

```python
# ✅ Good: Use consensus for critical decisions
result = orchestrator.orchestrate_with_consensus(
    task_type=TaskType.CODE_ANALYSIS,
    num_models=3  # Get multiple opinions
)

# ✅ Also Good: Single model for simple tasks
response = orchestrator.execute_llm_request(...)
# Don't overspend on consensus for simple tasks
```

### 5. Error Handling

```python
# ✅ Good: Handle failures gracefully
try:
    response = orchestrator.execute_llm_request(...)
except Exception as e:
    # Fallback to cheaper model
    response = orchestrator.execute_llm_request(
        model_key='gpt-3.5-turbo',
        ...
    )
```

## Metrics and Monitoring

### View Metrics

```python
metrics = orchestrator.get_metrics()

print(f"Total requests: {metrics['total_requests']}")
print(f"Cache hits: {metrics['cache_hits']}")
print(f"Cache hit rate: {metrics['cache_hit_rate']:.1%}")
print(f"Total cost: ${metrics['total_cost']:.4f}")
print(f"Avg cost/request: ${metrics['avg_cost_per_request']:.4f}")
print(f"Model usage: {metrics['model_usage']}")
```

### Optimization Tips

1. **High Cache Hit Rate** (>60%): Excellent! Users asking similar questions
2. **Low Cache Hit Rate** (<20%): Consider pre-warming cache with common queries
3. **High Total Cost**: Review model selection, use cheaper models for simple tasks
4. **Uneven Model Usage**: Some models may be over/under-utilized

## Troubleshooting

### Issue: High Costs

**Solutions**:
```python
# 1. Use budget constraints
model = orchestrator.select_best_model(
    task_type,
    budget=0.005  # Max cost
)

# 2. Enable caching
orchestrator.cache_enabled = True

# 3. Use cheaper models for simple tasks
if complexity == 'low':
    model = 'gpt-3.5-turbo'
```

### Issue: Slow Responses

**Solutions**:
```python
# 1. Use faster models
model = orchestrator.select_best_model(
    task_type,
    complexity='low'  # Faster, cheaper models
)

# 2. Reduce max_tokens
response = orchestrator.execute_llm_request(
    ...,
    max_tokens=1000  # Shorter responses
)

# 3. Avoid unnecessary consensus
# Use single model when appropriate
```

### Issue: Low Quality Results

**Solutions**:
```python
# 1. Use higher complexity models
model = orchestrator.select_best_model(
    task_type,
    complexity='high'
)

# 2. Use better prompting strategy
template_id = 'reasoning_tot'  # Tree-of-Thought

# 3. Use multi-model consensus
result = orchestrator.orchestrate_with_consensus(
    num_models=3
)
```

## Examples

### Complete Workflow Example

```python
from intelligent_llm_orchestrator import (
    IntelligentLLMOrchestrator,
    TaskType,
    PromptStrategy
)

# Initialize
orchestrator = IntelligentLLMOrchestrator()

# 1. Simple code generation
model = orchestrator.select_best_model(
    TaskType.CODE_GENERATION,
    complexity='medium'
)

system, user = orchestrator.build_prompt(
    'code_generation_cot',
    {'task_description': 'Create a REST API in Python'}
)

response = orchestrator.execute_llm_request(
    model_key=model,
    system_prompt=system,
    user_prompt=user
)

print(response.content)

# 2. Complex reasoning with consensus
result = orchestrator.orchestrate_with_consensus(
    task_type=TaskType.REASONING,
    template_id='reasoning_tot',
    variables={'problem': 'Design a scalable microservices architecture'},
    num_models=3
)

print(f"Synthesized answer: {result.synthesized_result}")
print(f"Confidence: {result.confidence:.0%}")

# 3. View metrics
metrics = orchestrator.get_metrics()
print(f"Total cost: ${metrics['total_cost']:.4f}")
print(f"Cache hit rate: {metrics['cache_hit_rate']:.1%}")
```

## See Also

- [Enhanced NLP System](ENHANCED_NLP.md)
- [Workflow Database](WORKFLOW_SYSTEM.md)
- [Comprehensive Integration](COMPREHENSIVE_INTEGRATION.md)
- [Context Engine](CONTEXT_ENGINE.md)
