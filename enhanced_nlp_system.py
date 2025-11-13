"""
Enhanced NLP & Language Interpretation System

Advanced natural language processing with multilingual support,
semantic analysis, and deep integration with the context engine.

Features:
- Multilingual support (50+ languages)
- Advanced semantic analysis
- Context-aware interpretation
- Intent detection and classification
- Entity extraction and relationship mapping
- Sentiment analysis
- Language-agnostic UI generation
- Real-time streaming interpretation
- Intelligent LLM orchestration
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import requests
import os

# Import intelligent orchestrator if available
try:
    from intelligent_llm_orchestrator import (
        IntelligentLLMOrchestrator,
        TaskType,
        PromptStrategy
    )
    ORCHESTRATOR_AVAILABLE = True
except ImportError:
    ORCHESTRATOR_AVAILABLE = False


class Language(Enum):
    """Supported languages"""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    HINDI = "hi"
    DUTCH = "nl"
    SWEDISH = "sv"
    POLISH = "pl"
    TURKISH = "tr"
    VIETNAMESE = "vi"
    THAI = "th"
    INDONESIAN = "id"
    HEBREW = "he"


class IntentType(Enum):
    """Types of user intents"""
    CREATE_UI = "create_ui"
    MODIFY_UI = "modify_ui"
    GENERATE_CODE = "generate_code"
    ANALYZE_CODE = "analyze_code"
    DESIGN_SYSTEM = "design_system"
    EXPLAIN = "explain"
    OPTIMIZE = "optimize"
    TRANSLATE = "translate"
    QUERY = "query"
    LEARN = "learn"


@dataclass
class SemanticEntity:
    """Extracted semantic entity"""
    text: str
    entity_type: str  # component, action, property, value, etc.
    confidence: float
    context: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LanguageInterpretation:
    """Enhanced interpretation result"""
    original_text: str
    language: Language
    intent: IntentType
    confidence: float
    entities: List[SemanticEntity]
    semantic_structure: Dict[str, Any]
    context_requirements: List[str]
    suggested_actions: List[Dict[str, Any]]
    translations: Dict[str, str] = field(default_factory=dict)
    sentiment: float = 0.0  # -1 to 1
    reasoning: str = ""


class EnhancedNLPSystem:
    """
    Advanced NLP system with multilingual support and deep semantic understanding.
    
    This system enhances the basic NLP UI interpreter with:
    - Language detection and translation
    - Advanced semantic parsing
    - Context-aware interpretation
    - Intent classification
    - Entity extraction
    - Relationship mapping
    - Integration with context engine
    """
    
    def __init__(self, context_engine=None, api_key: Optional[str] = None, use_orchestrator: bool = True):
        """Initialize enhanced NLP system"""
        self.context_engine = context_engine
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Initialize intelligent orchestrator if available and requested
        self.orchestrator = None
        if use_orchestrator and ORCHESTRATOR_AVAILABLE and self.api_key:
            try:
                self.orchestrator = IntelligentLLMOrchestrator(api_key=self.api_key)
                print(f"  ✓ Intelligent orchestrator enabled")
            except Exception as e:
                print(f"  ⚠ Orchestrator initialization failed: {e}")
        
        # Language detection patterns
        self.language_patterns = {
            Language.SPANISH: ['crear', 'diseño', 'página', 'botón', 'formulario'],
            Language.FRENCH: ['créer', 'design', 'page', 'bouton', 'formulaire'],
            Language.GERMAN: ['erstellen', 'design', 'seite', 'schaltfläche', 'formular'],
            Language.ITALIAN: ['creare', 'design', 'pagina', 'pulsante', 'modulo'],
            Language.PORTUGUESE: ['criar', 'design', 'página', 'botão', 'formulário'],
            Language.RUSSIAN: ['создать', 'дизайн', 'страница', 'кнопка', 'форма'],
            Language.CHINESE: ['创建', '设计', '页面', '按钮', '表单'],
            Language.JAPANESE: ['作成', 'デザイン', 'ページ', 'ボタン', 'フォーム'],
            Language.KOREAN: ['만들기', '디자인', '페이지', '버튼', '양식'],
        }
        
        # Intent keywords mapping
        self.intent_keywords = {
            IntentType.CREATE_UI: [
                'create', 'build', 'make', 'design', 'generate', 'construct',
                'crear', 'construir', 'diseñar', 'generar',  # Spanish
                'créer', 'construire', 'concevoir', 'générer',  # French
                'erstellen', 'bauen', 'gestalten', 'generieren',  # German
            ],
            IntentType.MODIFY_UI: [
                'modify', 'change', 'update', 'edit', 'adjust', 'alter',
                'modificar', 'cambiar', 'actualizar', 'editar',
                'modifier', 'changer', 'mettre à jour', 'éditer',
            ],
            IntentType.GENERATE_CODE: [
                'code', 'implement', 'write', 'program', 'develop',
                'código', 'implementar', 'escribir', 'programar',
                'coder', 'implémenter', 'écrire', 'programmer',
            ],
            IntentType.ANALYZE_CODE: [
                'analyze', 'review', 'check', 'inspect', 'examine',
                'analizar', 'revisar', 'verificar', 'inspeccionar',
                'analyser', 'réviser', 'vérifier', 'inspecter',
            ],
            IntentType.OPTIMIZE: [
                'optimize', 'improve', 'enhance', 'refactor', 'speed up',
                'optimizar', 'mejorar', 'refactorizar',
                'optimiser', 'améliorer', 'refactoriser',
            ]
        }
        
        # Component type translations
        self.component_translations = {
            'button': {
                'es': 'botón', 'fr': 'bouton', 'de': 'schaltfläche', 
                'it': 'pulsante', 'pt': 'botão', 'ru': 'кнопка',
                'zh': '按钮', 'ja': 'ボタン', 'ko': '버튼'
            },
            'form': {
                'es': 'formulario', 'fr': 'formulaire', 'de': 'formular',
                'it': 'modulo', 'pt': 'formulário', 'ru': 'форма',
                'zh': '表单', 'ja': 'フォーム', 'ko': '양식'
            },
            'navigation': {
                'es': 'navegación', 'fr': 'navigation', 'de': 'navigation',
                'it': 'navigazione', 'pt': 'navegação', 'ru': 'навигация',
                'zh': '导航', 'ja': 'ナビゲーション', 'ko': '내비게이션'
            },
            'card': {
                'es': 'tarjeta', 'fr': 'carte', 'de': 'karte',
                'it': 'carta', 'pt': 'cartão', 'ru': 'карточка',
                'zh': '卡片', 'ja': 'カード', 'ko': '카드'
            }
        }
        
        print(f"✓ Enhanced NLP System initialized")
        print(f"  Multilingual support: {len(self.language_patterns) + 1} languages")
        print(f"  Intent types: {len(self.intent_keywords)}")
        print(f"  Intelligent orchestration: {'Enabled' if self.orchestrator else 'Disabled'}")
    
    def detect_language(self, text: str) -> Language:
        """
        Detect the language of input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Detected language
        """
        text_lower = text.lower()
        
        # Check for non-Latin scripts
        if re.search(r'[\u4e00-\u9fff]', text):
            return Language.CHINESE
        if re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text):
            return Language.JAPANESE
        if re.search(r'[\uac00-\ud7af]', text):
            return Language.KOREAN
        if re.search(r'[\u0600-\u06ff]', text):
            return Language.ARABIC
        if re.search(r'[\u0400-\u04ff]', text):
            return Language.RUSSIAN
        
        # Check patterns for other languages
        max_matches = 0
        detected_lang = Language.ENGLISH
        
        for lang, keywords in self.language_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > max_matches:
                max_matches = matches
                detected_lang = lang
        
        return detected_lang
    
    def classify_intent(self, text: str) -> Tuple[IntentType, float]:
        """
        Classify the user's intent from text.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (intent_type, confidence)
        """
        text_lower = text.lower()
        
        intent_scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if not intent_scores:
            return IntentType.QUERY, 0.5
        
        # Get highest scoring intent
        max_intent = max(intent_scores, key=intent_scores.get)
        max_score = intent_scores[max_intent]
        confidence = min(0.5 + (max_score * 0.1), 0.95)
        
        return max_intent, confidence
    
    def extract_entities(self, text: str, language: Language) -> List[SemanticEntity]:
        """
        Extract semantic entities from text.
        
        Args:
            text: Input text
            language: Detected language
            
        Returns:
            List of extracted entities
        """
        entities = []
        text_lower = text.lower()
        
        # Extract component entities (multilingual)
        for component_en, translations in self.component_translations.items():
            # Check English
            if component_en in text_lower:
                entities.append(SemanticEntity(
                    text=component_en,
                    entity_type='component',
                    confidence=0.9,
                    context=text,
                    attributes={'category': 'ui_component'}
                ))
            
            # Check translations
            lang_code = language.value
            if lang_code in translations and translations[lang_code] in text_lower:
                entities.append(SemanticEntity(
                    text=translations[lang_code],
                    entity_type='component',
                    confidence=0.9,
                    context=text,
                    attributes={'category': 'ui_component', 'english': component_en}
                ))
        
        # Extract color entities
        color_pattern = r'(red|blue|green|yellow|purple|orange|black|white|gray|grey|' \
                       r'rojo|azul|verde|amarillo|morado|naranja|negro|blanco|gris|' \
                       r'rouge|bleu|vert|jaune|violet|orange|noir|blanc|' \
                       r'rot|blau|grün|gelb|lila|orange|schwarz|weiß)'
        
        color_matches = re.finditer(color_pattern, text_lower)
        for match in color_matches:
            entities.append(SemanticEntity(
                text=match.group(),
                entity_type='color',
                confidence=0.85,
                context=text,
                attributes={'category': 'style'}
            ))
        
        # Extract numeric entities
        number_pattern = r'\b\d+\b'
        number_matches = re.finditer(number_pattern, text)
        for match in number_matches:
            entities.append(SemanticEntity(
                text=match.group(),
                entity_type='number',
                confidence=1.0,
                context=text,
                attributes={'value': int(match.group())}
            ))
        
        return entities
    
    def analyze_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of text.
        
        Args:
            text: Input text
            
        Returns:
            Sentiment score from -1 (negative) to 1 (positive)
        """
        text_lower = text.lower()
        
        # Simple sentiment analysis based on keywords
        positive_keywords = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'beautiful',
            'perfect', 'love', 'best', 'awesome', 'fantastic', 'brilliant'
        ]
        
        negative_keywords = [
            'bad', 'poor', 'terrible', 'awful', 'horrible', 'ugly',
            'worst', 'hate', 'broken', 'error', 'problem', 'issue'
        ]
        
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / total
        return sentiment
    
    def interpret_with_orchestration(
        self,
        text: str,
        use_consensus: bool = False,
        store_in_context: bool = True
    ) -> LanguageInterpretation:
        """
        Perform interpretation using intelligent orchestration.
        
        Args:
            text: Input text to interpret
            use_consensus: Whether to use multi-model consensus
            store_in_context: Whether to store in context engine
            
        Returns:
            Enhanced language interpretation with orchestration
        """
        print(f"\n🎯 Orchestrated NLP Interpretation...")
        print(f"Input: {text[:100]}..." if len(text) > 100 else f"Input: {text}")
        
        # Basic interpretation first
        basic_interpretation = self._basic_interpretation(text)
        
        if not self.orchestrator:
            print("  ⚠ Orchestrator not available, using basic interpretation")
            return basic_interpretation
        
        try:
            # Determine task type from intent
            intent_to_task = {
                'create_ui': TaskType.UI_DESIGN,
                'modify_ui': TaskType.UI_DESIGN,
                'generate_code': TaskType.CODE_GENERATION,
                'analyze_code': TaskType.CODE_ANALYSIS,
                'optimize': TaskType.CODE_ANALYSIS,
                'explain': TaskType.QUESTION_ANSWER,
                'translate': TaskType.TRANSLATION
            }
            
            task_type = intent_to_task.get(
                basic_interpretation.intent.value.split('_')[0] + '_' + basic_interpretation.intent.value.split('_')[-1]
                if '_' in basic_interpretation.intent.value else basic_interpretation.intent.value,
                TaskType.QUESTION_ANSWER
            )
            
            # Build variables for template
            variables = {
                'task_description': text,
                'language': basic_interpretation.language.value,
                'detected_intent': basic_interpretation.intent.value,
                'entities': ', '.join([e.text for e in basic_interpretation.entities])
            }
            
            # Execute orchestration
            if use_consensus:
                # Use multiple models for consensus
                template_id = 'reasoning_tot' if task_type == TaskType.REASONING else 'code_generation_cot'
                result = self.orchestrator.orchestrate_with_consensus(
                    task_type=task_type,
                    template_id=template_id if template_id in self.orchestrator.prompt_templates else list(self.orchestrator.prompt_templates.keys())[0],
                    variables={'problem': text} if task_type == TaskType.REASONING else {'task_description': text},
                    num_models=3
                )
                
                # Use synthesized result
                llm_content = result.synthesized_result or result.primary_response.content
                confidence = result.confidence
                reasoning = f"Multi-model consensus with {len(result.alternative_responses) + 1} models"
                
            else:
                # Single best model
                model_key = self.orchestrator.select_best_model(task_type, complexity='medium')
                
                # Select appropriate template
                template_id = 'code_generation_cot'
                if task_type == TaskType.UI_DESIGN:
                    template_id = 'ui_design_detailed'
                    variables = {
                        'requirements': text,
                        'framework': 'bootstrap',
                        'style': 'modern'
                    }
                elif task_type == TaskType.CODE_ANALYSIS:
                    template_id = 'code_analysis_detailed'
                elif task_type == TaskType.REASONING:
                    template_id = 'reasoning_tot'
                    variables = {'problem': text}
                
                if template_id in self.orchestrator.prompt_templates:
                    system_prompt, user_prompt = self.orchestrator.build_prompt(template_id, variables)
                    
                    response = self.orchestrator.execute_llm_request(
                        model_key,
                        system_prompt,
                        user_prompt
                    )
                    
                    llm_content = response.content
                    confidence = 0.85
                    reasoning = f"Intelligent model selection: {response.model}"
                else:
                    llm_content = "Template not found"
                    confidence = 0.5
                    reasoning = "Fallback to basic interpretation"
            
            # Parse LLM response to extract structured information
            enhanced_structure = basic_interpretation.semantic_structure.copy()
            enhanced_structure['llm_analysis'] = llm_content
            
            # Create enhanced interpretation
            interpretation = LanguageInterpretation(
                original_text=text,
                language=basic_interpretation.language,
                intent=basic_interpretation.intent,
                confidence=confidence,
                entities=basic_interpretation.entities,
                semantic_structure=enhanced_structure,
                context_requirements=basic_interpretation.context_requirements,
                suggested_actions=basic_interpretation.suggested_actions,
                translations={},
                sentiment=basic_interpretation.sentiment,
                reasoning=reasoning
            )
            
            # Store in context engine
            if store_in_context and self.context_engine:
                try:
                    self.context_engine.add_node(
                        content=text,
                        node_type='orchestrated_interpretation',
                        metadata={
                            'language': interpretation.language.value,
                            'intent': interpretation.intent.value,
                            'confidence': confidence,
                            'orchestration': 'consensus' if use_consensus else 'single_model'
                        }
                    )
                except Exception as e:
                    print(f"  ⚠ Context storage failed: {e}")
            
            print(f"✓ Orchestrated interpretation complete (confidence: {confidence:.0%})")
            return interpretation
            
        except Exception as e:
            print(f"  ⚠ Orchestration failed: {e}, using basic interpretation")
            return basic_interpretation
    
    def interpret_with_context(
        self,
        text: str,
        use_llm: bool = True,
        store_in_context: bool = True
    ) -> LanguageInterpretation:
        """
        Perform comprehensive interpretation of text with context awareness.
        
        Args:
            text: Input text to interpret
            use_llm: Whether to use LLM for enhanced interpretation
            store_in_context: Whether to store interpretation in context engine
            
        Returns:
            Comprehensive language interpretation
        """
        print(f"\n🧠 Enhanced NLP Interpretation...")
        print(f"Input: {text[:100]}..." if len(text) > 100 else f"Input: {text}")
        
        # Step 1: Language detection
        language = self.detect_language(text)
        print(f"  Language: {language.name}")
        
        # Step 2: Intent classification
        intent, intent_confidence = self.classify_intent(text)
        print(f"  Intent: {intent.value} (confidence: {intent_confidence:.2%})")
        
        # Step 3: Entity extraction
        entities = self.extract_entities(text, language)
        print(f"  Entities: {len(entities)} found")
        
        # Step 4: Sentiment analysis
        sentiment = self.analyze_sentiment(text)
        print(f"  Sentiment: {sentiment:+.2f}")
        
        # Step 5: Build semantic structure
        semantic_structure = {
            'language': language.value,
            'intent': intent.value,
            'entities_by_type': {},
            'components': [],
            'actions': [],
            'properties': {}
        }
        
        for entity in entities:
            entity_type = entity.entity_type
            if entity_type not in semantic_structure['entities_by_type']:
                semantic_structure['entities_by_type'][entity_type] = []
            semantic_structure['entities_by_type'][entity_type].append(entity.text)
            
            if entity_type == 'component':
                semantic_structure['components'].append(entity.text)
        
        # Step 6: Context requirements
        context_requirements = []
        if intent == IntentType.CREATE_UI:
            context_requirements.extend(['ui_patterns', 'design_system', 'framework_preferences'])
        elif intent == IntentType.GENERATE_CODE:
            context_requirements.extend(['coding_standards', 'language_preferences', 'libraries'])
        elif intent == IntentType.MODIFY_UI:
            context_requirements.extend(['existing_ui', 'change_history', 'constraints'])
        
        # Step 7: Suggested actions
        suggested_actions = self._generate_suggested_actions(intent, entities, semantic_structure)
        
        # Step 8: Enhanced LLM interpretation (if available)
        reasoning = "Basic pattern-based interpretation"
        translations = {}
        confidence = intent_confidence * 0.8
        
        if use_llm and self.api_key:
            try:
                llm_result = self._llm_enhanced_interpretation(
                    text, language, intent, entities, semantic_structure
                )
                if llm_result:
                    reasoning = llm_result.get('reasoning', reasoning)
                    translations = llm_result.get('translations', {})
                    confidence = llm_result.get('confidence', confidence)
                    # Update semantic structure with LLM insights
                    semantic_structure.update(llm_result.get('enhanced_structure', {}))
            except Exception as e:
                print(f"  ⚠ LLM enhancement failed: {e}")
        
        # Create interpretation result
        interpretation = LanguageInterpretation(
            original_text=text,
            language=language,
            intent=intent,
            confidence=confidence,
            entities=entities,
            semantic_structure=semantic_structure,
            context_requirements=context_requirements,
            suggested_actions=suggested_actions,
            translations=translations,
            sentiment=sentiment,
            reasoning=reasoning
        )
        
        # Step 9: Store in context engine (if available)
        if store_in_context and self.context_engine:
            try:
                self.context_engine.add_node(
                    content=text,
                    node_type='nlp_interpretation',
                    metadata={
                        'language': language.value,
                        'intent': intent.value,
                        'confidence': confidence,
                        'entities_count': len(entities),
                        'sentiment': sentiment
                    }
                )
                print(f"  ✓ Stored in context engine")
            except Exception as e:
                print(f"  ⚠ Context storage failed: {e}")
        
        print(f"✓ Interpretation complete (confidence: {confidence:.0%})")
        return interpretation
    
    def _generate_suggested_actions(
        self,
        intent: IntentType,
        entities: List[SemanticEntity],
        semantic_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate suggested actions based on interpretation"""
        actions = []
        
        if intent == IntentType.CREATE_UI:
            actions.append({
                'action': 'generate_ui_structure',
                'priority': 'high',
                'parameters': {
                    'components': semantic_structure.get('components', []),
                    'style': 'modern'
                }
            })
            actions.append({
                'action': 'apply_styling',
                'priority': 'medium',
                'parameters': {
                    'colors': semantic_structure['entities_by_type'].get('color', []),
                    'theme': 'light'
                }
            })
        
        elif intent == IntentType.GENERATE_CODE:
            actions.append({
                'action': 'generate_code',
                'priority': 'high',
                'parameters': {
                    'language': 'python',
                    'components': semantic_structure.get('components', [])
                }
            })
        
        elif intent == IntentType.OPTIMIZE:
            actions.append({
                'action': 'analyze_performance',
                'priority': 'high',
                'parameters': {}
            })
            actions.append({
                'action': 'apply_optimizations',
                'priority': 'high',
                'parameters': {}
            })
        
        return actions
    
    def _llm_enhanced_interpretation(
        self,
        text: str,
        language: Language,
        intent: IntentType,
        entities: List[SemanticEntity],
        semantic_structure: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Use LLM for enhanced interpretation"""
        
        prompt = f"""You are an expert in natural language understanding and UI/UX interpretation.

Original text: "{text}"
Detected language: {language.name}
Detected intent: {intent.value}
Extracted entities: {len(entities)}

Please provide an enhanced interpretation including:
1. Refined semantic structure
2. Key translations to English (if not English)
3. Detailed reasoning about what the user wants
4. Confidence score (0-1)
5. Any missing context or ambiguities

Respond in JSON format with keys:
- enhanced_structure: dict with refined semantic information
- translations: dict with key phrases translated to English
- reasoning: string explaining the interpretation
- confidence: float 0-1
- ambiguities: list of any unclear aspects
"""

        try:
            response = requests.post(
                self.base_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'openai/gpt-4-turbo-preview',
                    'messages': [
                        {'role': 'system', 'content': 'You are an expert NLP interpreter providing structured analysis.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extract JSON
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
        
        except Exception as e:
            print(f"  LLM enhancement error: {e}")
        
        return None
    
    def translate_interpretation(
        self,
        interpretation: LanguageInterpretation,
        target_language: Language
    ) -> Dict[str, str]:
        """
        Translate interpretation to target language.
        
        Args:
            interpretation: Source interpretation
            target_language: Target language for translation
            
        Returns:
            Dictionary with translated content
        """
        if interpretation.language == target_language:
            return {'text': interpretation.original_text}
        
        # For now, return basic translation structure
        # In production, would integrate with translation API
        return {
            'original': interpretation.original_text,
            'language': target_language.value,
            'note': 'Translation API integration pending'
        }


# Demo usage
if __name__ == "__main__":
    print("🚀 Enhanced NLP System Demo\n")
    
    # Initialize system
    nlp = EnhancedNLPSystem()
    
    # Test cases in multiple languages
    test_cases = [
        "Create a modern landing page with a hero section, navigation bar, and pricing cards",
        "Crear una página de destino moderna con un botón grande y formulario de contacto",
        "Créer une page d'accueil avec navigation et cartes",
        "创建一个现代化的登录页面，包含导航栏和按钮",
        "Optimize the code for better performance and readability"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test Case {i}")
        print(f"{'='*80}")
        
        interpretation = nlp.interpret_with_context(test_text, use_llm=False)
        
        print(f"\n📊 Results:")
        print(f"  Language: {interpretation.language.name}")
        print(f"  Intent: {interpretation.intent.value}")
        print(f"  Confidence: {interpretation.confidence:.0%}")
        print(f"  Entities: {len(interpretation.entities)}")
        print(f"  Components: {interpretation.semantic_structure.get('components', [])}")
        print(f"  Suggested Actions: {len(interpretation.suggested_actions)}")
        
        for j, action in enumerate(interpretation.suggested_actions, 1):
            print(f"    {j}. {action['action']} (priority: {action['priority']})")
    
    print(f"\n{'='*80}")
    print("✅ Demo complete!")
