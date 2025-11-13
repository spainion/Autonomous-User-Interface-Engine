"""
Intelligent LLM Orchestrator with Advanced Prompting

Advanced orchestration system for OpenRouter API with intelligent prompting,
model selection, and multi-model synthesis.

Features:
- Intelligent prompt engineering and optimization
- Dynamic model selection based on task type
- Multi-model orchestration and consensus
- Result synthesis and quality scoring
- Fallback strategies and error handling
- Cost optimization
- Performance tracking
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import requests


class TaskType(Enum):
    """Types of tasks for model selection"""
    CODE_GENERATION = "code_generation"
    CODE_ANALYSIS = "code_analysis"
    UI_DESIGN = "ui_design"
    CREATIVE_WRITING = "creative_writing"
    REASONING = "reasoning"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    QUESTION_ANSWER = "question_answer"
    DATA_EXTRACTION = "data_extraction"
    CLASSIFICATION = "classification"


class PromptStrategy(Enum):
    """Prompting strategies"""
    ZERO_SHOT = "zero_shot"
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHT = "tree_of_thought"
    REACT = "react"  # Reason + Act
    SELF_CONSISTENCY = "self_consistency"
    INSTRUCTION_FOLLOWING = "instruction_following"


@dataclass
class ModelConfig:
    """Configuration for an LLM model"""
    model_id: str
    display_name: str
    provider: str
    strengths: List[TaskType]
    cost_per_1k_tokens: float
    max_tokens: int
    context_window: int
    best_temperature: float = 0.7
    supports_functions: bool = False


@dataclass
class PromptTemplate:
    """Template for prompts"""
    template_id: str
    task_type: TaskType
    strategy: PromptStrategy
    system_prompt: str
    user_prompt_template: str
    examples: List[Dict[str, str]] = field(default_factory=list)
    variables: List[str] = field(default_factory=list)


@dataclass
class LLMResponse:
    """Response from LLM"""
    model: str
    content: str
    tokens_used: int
    latency: float
    cost: float
    quality_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OrchestrationResult:
    """Result from orchestration"""
    task_type: TaskType
    strategy: PromptStrategy
    primary_response: LLMResponse
    alternative_responses: List[LLMResponse] = field(default_factory=list)
    synthesized_result: Optional[str] = None
    confidence: float = 0.0
    total_cost: float = 0.0
    total_latency: float = 0.0


class IntelligentLLMOrchestrator:
    """
    Advanced orchestration system for OpenRouter API with intelligent prompting.
    
    Features:
    - Intelligent model selection based on task
    - Advanced prompting strategies (CoT, few-shot, etc.)
    - Multi-model orchestration with consensus
    - Result synthesis and quality assessment
    - Cost optimization
    - Caching and performance tracking
    """
    
    def __init__(self, api_key: Optional[str] = None, cache_enabled: bool = True):
        """Initialize orchestrator"""
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.cache_enabled = cache_enabled
        self.cache: Dict[str, LLMResponse] = {}
        
        # Model configurations
        self.models = self._initialize_models()
        
        # Prompt templates
        self.prompt_templates = self._initialize_prompt_templates()
        
        # Performance tracking
        self.metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'total_cost': 0.0,
            'avg_latency': 0.0,
            'model_usage': {}
        }
        
        print(f"✓ Intelligent LLM Orchestrator initialized")
        print(f"  Available models: {len(self.models)}")
        print(f"  Prompt templates: {len(self.prompt_templates)}")
        print(f"  Caching: {'Enabled' if cache_enabled else 'Disabled'}")
    
    def _initialize_models(self) -> Dict[str, ModelConfig]:
        """Initialize model configurations"""
        return {
            # OpenAI Models
            'gpt-4-turbo': ModelConfig(
                model_id='openai/gpt-4-turbo-preview',
                display_name='GPT-4 Turbo',
                provider='OpenAI',
                strengths=[TaskType.CODE_GENERATION, TaskType.REASONING, TaskType.CODE_ANALYSIS],
                cost_per_1k_tokens=0.01,
                max_tokens=4096,
                context_window=128000,
                best_temperature=0.7,
                supports_functions=True
            ),
            'gpt-4': ModelConfig(
                model_id='openai/gpt-4',
                display_name='GPT-4',
                provider='OpenAI',
                strengths=[TaskType.REASONING, TaskType.CODE_ANALYSIS, TaskType.CREATIVE_WRITING],
                cost_per_1k_tokens=0.03,
                max_tokens=8192,
                context_window=8192,
                best_temperature=0.7,
                supports_functions=True
            ),
            'gpt-3.5-turbo': ModelConfig(
                model_id='openai/gpt-3.5-turbo',
                display_name='GPT-3.5 Turbo',
                provider='OpenAI',
                strengths=[TaskType.SUMMARIZATION, TaskType.TRANSLATION, TaskType.QUESTION_ANSWER],
                cost_per_1k_tokens=0.0015,
                max_tokens=4096,
                context_window=16385,
                best_temperature=0.7,
                supports_functions=True
            ),
            
            # Anthropic Models
            'claude-3-opus': ModelConfig(
                model_id='anthropic/claude-3-opus',
                display_name='Claude 3 Opus',
                provider='Anthropic',
                strengths=[TaskType.CODE_GENERATION, TaskType.REASONING, TaskType.CREATIVE_WRITING],
                cost_per_1k_tokens=0.015,
                max_tokens=4096,
                context_window=200000,
                best_temperature=0.7,
                supports_functions=False
            ),
            'claude-3-sonnet': ModelConfig(
                model_id='anthropic/claude-3-sonnet',
                display_name='Claude 3 Sonnet',
                provider='Anthropic',
                strengths=[TaskType.CODE_ANALYSIS, TaskType.UI_DESIGN, TaskType.REASONING],
                cost_per_1k_tokens=0.003,
                max_tokens=4096,
                context_window=200000,
                best_temperature=0.7,
                supports_functions=False
            ),
            
            # Google Models
            'gemini-pro': ModelConfig(
                model_id='google/gemini-pro',
                display_name='Gemini Pro',
                provider='Google',
                strengths=[TaskType.REASONING, TaskType.DATA_EXTRACTION, TaskType.CLASSIFICATION],
                cost_per_1k_tokens=0.00025,
                max_tokens=2048,
                context_window=32000,
                best_temperature=0.7,
                supports_functions=False
            ),
            
            # Mistral Models
            'mixtral-8x7b': ModelConfig(
                model_id='mistralai/mixtral-8x7b-instruct',
                display_name='Mixtral 8x7B',
                provider='Mistral',
                strengths=[TaskType.CODE_GENERATION, TaskType.SUMMARIZATION, TaskType.TRANSLATION],
                cost_per_1k_tokens=0.00027,
                max_tokens=4096,
                context_window=32000,
                best_temperature=0.7,
                supports_functions=False
            ),
            
            # Meta Models
            'llama-3-70b': ModelConfig(
                model_id='meta-llama/llama-3-70b-instruct',
                display_name='Llama 3 70B',
                provider='Meta',
                strengths=[TaskType.CODE_GENERATION, TaskType.REASONING, TaskType.QUESTION_ANSWER],
                cost_per_1k_tokens=0.00059,
                max_tokens=4096,
                context_window=8000,
                best_temperature=0.7,
                supports_functions=False
            )
        }
    
    def _initialize_prompt_templates(self) -> Dict[str, PromptTemplate]:
        """Initialize prompt templates"""
        templates = {}
        
        # Code Generation Template
        templates['code_generation_cot'] = PromptTemplate(
            template_id='code_generation_cot',
            task_type=TaskType.CODE_GENERATION,
            strategy=PromptStrategy.CHAIN_OF_THOUGHT,
            system_prompt="""You are an expert software engineer. When generating code:
1. First, understand the requirements clearly
2. Plan the implementation approach
3. Consider edge cases and error handling
4. Write clean, maintainable code with comments
5. Explain your reasoning at each step""",
            user_prompt_template="""Task: {task_description}

Let's approach this step by step:
1. What are the key requirements?
2. What's the best approach?
3. What edge cases should we handle?
4. Implementation:

Please provide the complete solution with explanations.""",
            variables=['task_description']
        )
        
        # UI Design Template
        templates['ui_design_detailed'] = PromptTemplate(
            template_id='ui_design_detailed',
            task_type=TaskType.UI_DESIGN,
            strategy=PromptStrategy.INSTRUCTION_FOLLOWING,
            system_prompt="""You are an expert UI/UX designer and front-end developer. 
Create beautiful, accessible, and responsive user interfaces following modern design principles.""",
            user_prompt_template="""Design Requirements: {requirements}

Please provide:
1. **Layout Structure**: Describe the overall layout and sections
2. **Component Breakdown**: List all UI components needed
3. **Visual Design**: Color scheme, typography, spacing
4. **Interactions**: User interactions and animations
5. **Accessibility**: ARIA labels and keyboard navigation
6. **Responsive Design**: Mobile, tablet, desktop breakpoints
7. **Implementation**: HTML/CSS/JavaScript code

Target Framework: {framework}
Style Preference: {style}""",
            variables=['requirements', 'framework', 'style'],
            examples=[
                {
                    'input': 'Create a login form',
                    'output': 'Here\'s a modern, accessible login form design...'
                }
            ]
        )
        
        # Code Analysis Template
        templates['code_analysis_detailed'] = PromptTemplate(
            template_id='code_analysis_detailed',
            task_type=TaskType.CODE_ANALYSIS,
            strategy=PromptStrategy.CHAIN_OF_THOUGHT,
            system_prompt="""You are a senior code reviewer with expertise in software architecture, 
security, and best practices. Provide thorough, constructive analysis.""",
            user_prompt_template="""Code to analyze:
```{language}
{code}
```

Please analyze this code systematically:

1. **Functionality**: Does it work correctly? Are there bugs?
2. **Code Quality**: Readability, maintainability, organization
3. **Performance**: Efficiency, optimization opportunities
4. **Security**: Vulnerabilities, input validation
5. **Best Practices**: Following language conventions
6. **Suggestions**: Specific improvements with examples

Be specific and provide code examples for improvements.""",
            variables=['language', 'code']
        )
        
        # Reasoning Template
        templates['reasoning_tot'] = PromptTemplate(
            template_id='reasoning_tot',
            task_type=TaskType.REASONING,
            strategy=PromptStrategy.TREE_OF_THOUGHT,
            system_prompt="""You are an expert problem solver. Use systematic reasoning to explore 
multiple solution paths and evaluate them.""",
            user_prompt_template="""Problem: {problem}

Let's explore this systematically using tree-of-thought reasoning:

**Step 1: Understanding**
- What is being asked?
- What information do we have?
- What are the constraints?

**Step 2: Solution Approaches**
Generate 3 different approaches:
- Approach A: [describe]
- Approach B: [describe]
- Approach C: [describe]

**Step 3: Evaluation**
For each approach, evaluate:
- Feasibility
- Efficiency
- Tradeoffs

**Step 4: Best Solution**
Select and explain the best approach with detailed reasoning.

**Step 5: Implementation**
Provide concrete steps or code.""",
            variables=['problem']
        )
        
        # Few-Shot Learning Template
        templates['classification_few_shot'] = PromptTemplate(
            template_id='classification_few_shot',
            task_type=TaskType.CLASSIFICATION,
            strategy=PromptStrategy.FEW_SHOT,
            system_prompt="""You are a classification expert. Learn from examples and classify new instances accurately.""",
            user_prompt_template="""Task: Classify the following item

Examples:
{examples}

Now classify:
Input: {input}
Classification: """,
            variables=['examples', 'input'],
            examples=[
                {'input': 'Create a button', 'output': 'UI_COMPONENT'},
                {'input': 'Fix the bug', 'output': 'CODE_MODIFICATION'},
                {'input': 'Explain how it works', 'output': 'DOCUMENTATION'}
            ]
        )
        
        # ReAct Template (Reasoning + Acting)
        templates['problem_solving_react'] = PromptTemplate(
            template_id='problem_solving_react',
            task_type=TaskType.REASONING,
            strategy=PromptStrategy.REACT,
            system_prompt="""You are an AI assistant that reasons and acts. Use this format:
Thought: [your reasoning]
Action: [action to take]
Observation: [result of action]
... (repeat as needed)
Answer: [final answer]""",
            user_prompt_template="""Question: {question}

Solve this step-by-step using reasoning and actions:

Thought: Let me break down this problem...
Action: Identify the key components
Observation: The key components are...
Thought: Now I need to...
Action: Analyze relationships
Observation: The relationships show...
Answer: Based on my analysis, the solution is...""",
            variables=['question']
        )
        
        return templates
    
    def select_best_model(
        self,
        task_type: TaskType,
        complexity: str = 'medium',
        budget: Optional[float] = None
    ) -> str:
        """
        Select the best model for a given task.
        
        Args:
            task_type: Type of task
            complexity: 'low', 'medium', or 'high'
            budget: Optional budget constraint (cost per 1k tokens)
            
        Returns:
            Model key
        """
        # Filter models by task strength
        suitable_models = [
            (key, model) for key, model in self.models.items()
            if task_type in model.strengths
        ]
        
        if not suitable_models:
            # Fallback to GPT-4 for unknown tasks
            return 'gpt-4-turbo'
        
        # Apply budget constraint
        if budget:
            suitable_models = [
                (key, model) for key, model in suitable_models
                if model.cost_per_1k_tokens <= budget
            ]
        
        if not suitable_models:
            # Return cheapest model if budget too low
            return min(self.models.items(), key=lambda x: x[1].cost_per_1k_tokens)[0]
        
        # Select based on complexity
        if complexity == 'high':
            # Choose most capable (usually most expensive)
            return max(suitable_models, key=lambda x: x[1].cost_per_1k_tokens)[0]
        elif complexity == 'low':
            # Choose cheapest suitable model
            return min(suitable_models, key=lambda x: x[1].cost_per_1k_tokens)[0]
        else:
            # Choose middle ground
            sorted_models = sorted(suitable_models, key=lambda x: x[1].cost_per_1k_tokens)
            return sorted_models[len(sorted_models) // 2][0]
    
    def build_prompt(
        self,
        template_id: str,
        variables: Dict[str, str],
        include_examples: bool = True
    ) -> Tuple[str, str]:
        """
        Build prompt from template.
        
        Args:
            template_id: ID of template to use
            variables: Values for template variables
            include_examples: Whether to include few-shot examples
            
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        template = self.prompt_templates.get(template_id)
        if not template:
            raise ValueError(f"Template '{template_id}' not found")
        
        # Validate variables
        missing = set(template.variables) - set(variables.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")
        
        # Build user prompt
        user_prompt = template.user_prompt_template
        for var, value in variables.items():
            user_prompt = user_prompt.replace(f'{{{var}}}', str(value))
        
        # Add examples if few-shot
        if include_examples and template.strategy == PromptStrategy.FEW_SHOT and template.examples:
            examples_text = '\n'.join([
                f"Input: {ex['input']}\nOutput: {ex['output']}"
                for ex in template.examples
            ])
            user_prompt = user_prompt.replace('{examples}', examples_text)
        
        return template.system_prompt, user_prompt
    
    def _get_cache_key(self, model: str, messages: List[Dict], temperature: float) -> str:
        """Generate cache key for request"""
        content = json.dumps({
            'model': model,
            'messages': messages,
            'temperature': temperature
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def execute_llm_request(
        self,
        model_key: str,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: int = 2000
    ) -> LLMResponse:
        """
        Execute LLM request with caching.
        
        Args:
            model_key: Key of model to use
            system_prompt: System prompt
            user_prompt: User prompt
            temperature: Optional temperature override
            max_tokens: Maximum tokens to generate
            
        Returns:
            LLM response
        """
        model_config = self.models.get(model_key)
        if not model_config:
            raise ValueError(f"Model '{model_key}' not found")
        
        # Build messages
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        
        # Use model's best temperature if not specified
        temp = temperature if temperature is not None else model_config.best_temperature
        
        # Check cache
        cache_key = self._get_cache_key(model_config.model_id, messages, temp)
        if self.cache_enabled and cache_key in self.cache:
            self.metrics['cache_hits'] += 1
            print(f"  ⚡ Cache hit for {model_config.display_name}")
            return self.cache[cache_key]
        
        # Execute request
        start_time = time.time()
        
        try:
            response = requests.post(
                self.base_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': model_config.model_id,
                    'messages': messages,
                    'temperature': temp,
                    'max_tokens': max_tokens
                },
                timeout=60
            )
            
            latency = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                tokens_used = result.get('usage', {}).get('total_tokens', 0)
                cost = (tokens_used / 1000) * model_config.cost_per_1k_tokens
                
                llm_response = LLMResponse(
                    model=model_config.display_name,
                    content=content,
                    tokens_used=tokens_used,
                    latency=latency,
                    cost=cost,
                    metadata={
                        'model_id': model_config.model_id,
                        'provider': model_config.provider,
                        'temperature': temp
                    }
                )
                
                # Cache response
                if self.cache_enabled:
                    self.cache[cache_key] = llm_response
                
                # Update metrics
                self.metrics['total_requests'] += 1
                self.metrics['total_cost'] += cost
                self.metrics['model_usage'][model_key] = self.metrics['model_usage'].get(model_key, 0) + 1
                
                return llm_response
            
            else:
                raise Exception(f"API error: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"  ❌ Request failed: {e}")
            raise
    
    def orchestrate_with_consensus(
        self,
        task_type: TaskType,
        template_id: str,
        variables: Dict[str, str],
        num_models: int = 3,
        temperature: float = 0.7
    ) -> OrchestrationResult:
        """
        Orchestrate multiple models and synthesize results with consensus.
        
        Args:
            task_type: Type of task
            template_id: Prompt template to use
            variables: Template variables
            num_models: Number of models to use
            temperature: Temperature for generation
            
        Returns:
            Orchestration result with consensus
        """
        print(f"\n🎭 Multi-Model Orchestration")
        print(f"{'='*80}")
        print(f"Task: {task_type.value}")
        print(f"Strategy: {num_models} models with consensus")
        
        # Select multiple suitable models
        suitable_models = [
            key for key, model in self.models.items()
            if task_type in model.strengths
        ][:num_models]
        
        if len(suitable_models) < num_models:
            # Fill with general-purpose models
            suitable_models.extend([
                key for key in ['gpt-4-turbo', 'claude-3-sonnet', 'gemini-pro']
                if key not in suitable_models
            ][:num_models - len(suitable_models)])
        
        # Build prompt
        system_prompt, user_prompt = self.build_prompt(template_id, variables)
        
        # Execute requests in parallel (simulated)
        responses = []
        for model_key in suitable_models:
            print(f"\n  📡 Querying {self.models[model_key].display_name}...")
            try:
                response = self.execute_llm_request(
                    model_key,
                    system_prompt,
                    user_prompt,
                    temperature=temperature
                )
                responses.append(response)
                print(f"  ✓ Response received ({response.tokens_used} tokens, {response.latency:.2f}s)")
            except Exception as e:
                print(f"  ⚠ Skipped due to error: {e}")
        
        if not responses:
            raise Exception("All model requests failed")
        
        # Primary response (first/best)
        primary_response = responses[0]
        
        # Synthesize if multiple responses
        synthesized = None
        confidence = 0.7
        
        if len(responses) > 1:
            print(f"\n  🔄 Synthesizing {len(responses)} responses...")
            synthesized = self._synthesize_responses(responses, task_type)
            confidence = self._calculate_consensus_confidence(responses)
            print(f"  ✓ Synthesis complete (confidence: {confidence:.0%})")
        
        result = OrchestrationResult(
            task_type=task_type,
            strategy=self.prompt_templates[template_id].strategy,
            primary_response=primary_response,
            alternative_responses=responses[1:],
            synthesized_result=synthesized,
            confidence=confidence,
            total_cost=sum(r.cost for r in responses),
            total_latency=max(r.latency for r in responses)
        )
        
        print(f"\n{'='*80}")
        print(f"✅ Orchestration complete!")
        print(f"  Total cost: ${result.total_cost:.4f}")
        print(f"  Max latency: {result.total_latency:.2f}s")
        print(f"  Confidence: {result.confidence:.0%}")
        
        return result
    
    def _synthesize_responses(
        self,
        responses: List[LLMResponse],
        task_type: TaskType
    ) -> str:
        """Synthesize multiple responses into one"""
        if task_type == TaskType.CODE_GENERATION:
            # For code, prefer the longest/most complete response
            return max(responses, key=lambda r: len(r.content)).content
        
        elif task_type == TaskType.REASONING:
            # Combine insights from all responses
            synthesis = "# Synthesized Analysis\n\n"
            for i, response in enumerate(responses, 1):
                synthesis += f"## Perspective {i} ({response.model}):\n{response.content}\n\n"
            return synthesis
        
        else:
            # Default: return primary response
            return responses[0].content
    
    def _calculate_consensus_confidence(self, responses: List[LLMResponse]) -> float:
        """Calculate confidence based on response agreement"""
        if len(responses) < 2:
            return 0.7
        
        # Simple similarity check based on length and structure
        lengths = [len(r.content) for r in responses]
        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        
        # Lower variance = higher confidence
        confidence = max(0.5, min(0.95, 1.0 - (variance / (avg_length ** 2))))
        return confidence
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            **self.metrics,
            'cache_hit_rate': self.metrics['cache_hits'] / max(self.metrics['total_requests'], 1),
            'avg_cost_per_request': self.metrics['total_cost'] / max(self.metrics['total_requests'], 1)
        }


# Demo usage
if __name__ == "__main__":
    print("🚀 Intelligent LLM Orchestrator Demo\n")
    
    # Initialize orchestrator
    orchestrator = IntelligentLLMOrchestrator()
    
    # Test 1: Model Selection
    print("="*80)
    print("TEST 1: Intelligent Model Selection")
    print("="*80)
    
    for task_type in [TaskType.CODE_GENERATION, TaskType.UI_DESIGN, TaskType.REASONING]:
        for complexity in ['low', 'medium', 'high']:
            model = orchestrator.select_best_model(task_type, complexity)
            print(f"{task_type.value:20s} ({complexity:6s}): {orchestrator.models[model].display_name}")
    
    # Test 2: Build Prompt
    print("\n" + "="*80)
    print("TEST 2: Intelligent Prompt Building")
    print("="*80)
    
    system, user = orchestrator.build_prompt(
        'code_generation_cot',
        {'task_description': 'Create a Python function to calculate fibonacci numbers'}
    )
    print(f"System Prompt:\n{system}\n")
    print(f"User Prompt:\n{user[:200]}...\n")
    
    # Test 3: View Available Templates
    print("="*80)
    print("TEST 3: Available Prompt Templates")
    print("="*80)
    
    for template_id, template in orchestrator.prompt_templates.items():
        print(f"  {template_id:30s} - {template.strategy.value:20s} - {template.task_type.value}")
    
    # Test 4: Metrics
    print("\n" + "="*80)
    print("TEST 4: Performance Metrics")
    print("="*80)
    
    metrics = orchestrator.get_metrics()
    print(json.dumps(metrics, indent=2))
    
    print("\n✅ Demo complete!")
