"""
Context Compression for Autonomous UI Engine
Phase 6: Innovation - AI Features

Optimizes and compresses context to fit within token limits while preserving important information.
"""

import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio

logger = logging.getLogger(__name__)


class CompressionStrategy(Enum):
    """Context compression strategies."""
    TRUNCATE = "truncate"               # Simple truncation
    SUMMARIZE = "summarize"             # Summarize long sections
    EXTRACT_KEY_INFO = "extract"        # Extract key information
    HIERARCHICAL = "hierarchical"       # Hierarchical compression
    SEMANTIC = "semantic"               # Semantic compression


@dataclass
class CompressionResult:
    """Result of context compression."""
    original_text: str
    compressed_text: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    preserved_information: float  # 0-1 estimate
    strategy_used: CompressionStrategy
    metadata: Dict[str, Any]


class ContextCompressor:
    """
    Compresses context to fit within token limits while preserving key information.
    """
    
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Initialize the context compressor.
        
        Args:
            llm_client: Optional LLM client for advanced compression
        """
        self.llm_client = llm_client
        self.compression_history: List[Dict[str, Any]] = []
        
    async def compress(
        self,
        text: str,
        max_tokens: int,
        strategy: Optional[CompressionStrategy] = None,
        preserve_sections: Optional[List[str]] = None
    ) -> CompressionResult:
        """
        Compress text to fit within token limit.
        
        Args:
            text: Text to compress
            max_tokens: Maximum number of tokens allowed
            strategy: Optional specific compression strategy
            preserve_sections: Optional list of section headers to preserve
            
        Returns:
            CompressionResult with compressed text and metadata
        """
        try:
            logger.info(f"Compressing text from {len(text)} characters...")
            
            # Estimate current tokens
            current_tokens = self._estimate_tokens(text)
            
            # If already within limit, return as-is
            if current_tokens <= max_tokens:
                return CompressionResult(
                    original_text=text,
                    compressed_text=text,
                    original_tokens=current_tokens,
                    compressed_tokens=current_tokens,
                    compression_ratio=1.0,
                    preserved_information=1.0,
                    strategy_used=CompressionStrategy.TRUNCATE,
                    metadata={"no_compression_needed": True}
                )
            
            # Select strategy if not specified
            if strategy is None:
                strategy = self._select_compression_strategy(
                    text, current_tokens, max_tokens
                )
            
            # Apply compression
            compressed_text, metadata = await self._apply_compression(
                text, max_tokens, strategy, preserve_sections or []
            )
            
            # Create result
            compressed_tokens = self._estimate_tokens(compressed_text)
            result = CompressionResult(
                original_text=text,
                compressed_text=compressed_text,
                original_tokens=current_tokens,
                compressed_tokens=compressed_tokens,
                compression_ratio=compressed_tokens / current_tokens if current_tokens > 0 else 1.0,
                preserved_information=self._estimate_information_preservation(
                    text, compressed_text
                ),
                strategy_used=strategy,
                metadata=metadata
            )
            
            # Log compression
            self._log_compression(result)
            
            logger.info(
                f"Compressed from {current_tokens} to {compressed_tokens} tokens "
                f"({result.compression_ratio:.2%})"
            )
            return result
            
        except Exception as e:
            logger.error(f"Error compressing context: {e}")
            # Return truncated version as fallback
            truncated = self._truncate_to_tokens(text, max_tokens)
            return CompressionResult(
                original_text=text,
                compressed_text=truncated,
                original_tokens=self._estimate_tokens(text),
                compressed_tokens=self._estimate_tokens(truncated),
                compression_ratio=len(truncated) / len(text) if text else 1.0,
                preserved_information=0.5,
                strategy_used=CompressionStrategy.TRUNCATE,
                metadata={"error": str(e)}
            )
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate number of tokens in text (rough approximation)."""
        # Rough estimate: ~4 characters per token for English text
        return len(text) // 4 + len(text.split())
    
    def _select_compression_strategy(
        self,
        text: str,
        current_tokens: int,
        max_tokens: int
    ) -> CompressionStrategy:
        """Select appropriate compression strategy."""
        compression_needed = 1.0 - (max_tokens / current_tokens)
        
        # Small compression needed - simple truncation
        if compression_needed < 0.2:
            return CompressionStrategy.TRUNCATE
        
        # Moderate compression - extract key info
        elif compression_needed < 0.5:
            return CompressionStrategy.EXTRACT_KEY_INFO
        
        # Heavy compression needed - summarize
        elif compression_needed < 0.7:
            return CompressionStrategy.SUMMARIZE
        
        # Very heavy compression - hierarchical
        else:
            return CompressionStrategy.HIERARCHICAL
    
    async def _apply_compression(
        self,
        text: str,
        max_tokens: int,
        strategy: CompressionStrategy,
        preserve_sections: List[str]
    ) -> Tuple[str, Dict[str, Any]]:
        """Apply specific compression strategy."""
        if strategy == CompressionStrategy.TRUNCATE:
            return self._compress_truncate(text, max_tokens, preserve_sections)
        
        elif strategy == CompressionStrategy.EXTRACT_KEY_INFO:
            return self._compress_extract_key_info(text, max_tokens, preserve_sections)
        
        elif strategy == CompressionStrategy.SUMMARIZE:
            return await self._compress_summarize(text, max_tokens, preserve_sections)
        
        elif strategy == CompressionStrategy.HIERARCHICAL:
            return self._compress_hierarchical(text, max_tokens, preserve_sections)
        
        elif strategy == CompressionStrategy.SEMANTIC:
            return await self._compress_semantic(text, max_tokens, preserve_sections)
        
        else:
            return self._compress_truncate(text, max_tokens, preserve_sections)
    
    def _compress_truncate(
        self,
        text: str,
        max_tokens: int,
        preserve_sections: List[str]
    ) -> Tuple[str, Dict[str, Any]]:
        """Simple truncation with section preservation."""
        # Extract and preserve specified sections
        preserved_text = []
        remaining_text = text
        
        for section in preserve_sections:
            match = re.search(
                rf'(#+\s*{re.escape(section)}.*?)(?=\n#+\s|\Z)',
                text,
                re.DOTALL | re.IGNORECASE
            )
            if match:
                preserved_text.append(match.group(1))
                remaining_text = remaining_text.replace(match.group(1), '')
        
        # Calculate tokens for preserved sections
        preserved_tokens = sum(self._estimate_tokens(t) for t in preserved_text)
        remaining_token_budget = max_tokens - preserved_tokens
        
        # Truncate remaining text
        truncated_remaining = self._truncate_to_tokens(remaining_text, remaining_token_budget)
        
        # Combine
        final_text = '\n\n'.join(preserved_text + [truncated_remaining])
        
        return final_text, {
            "method": "truncate",
            "preserved_sections": len(preserve_sections)
        }
    
    def _compress_extract_key_info(
        self,
        text: str,
        max_tokens: int,
        preserve_sections: List[str]
    ) -> Tuple[str, Dict[str, Any]]:
        """Extract key information from text."""
        # Extract important elements
        key_elements = []
        
        # Extract headers
        headers = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
        if headers:
            key_elements.append("# Key Topics\n" + '\n'.join(f"- {h}" for h in headers[:10]))
        
        # Extract bullet points
        bullets = re.findall(r'^\s*[-*]\s+(.+)$', text, re.MULTILINE)
        if bullets:
            key_elements.append("\n# Key Points\n" + '\n'.join(f"- {b}" for b in bullets[:15]))
        
        # Extract numbered lists
        numbered = re.findall(r'^\s*\d+\.\s+(.+)$', text, re.MULTILINE)
        if numbered:
            key_elements.append("\n# Steps/Requirements\n" + '\n'.join(f"{i+1}. {n}" for i, n in enumerate(numbered[:10])))
        
        # Extract code blocks
        code_blocks = re.findall(r'```[\w]*\n(.*?)```', text, re.DOTALL)
        if code_blocks:
            key_elements.append(f"\n# Code Snippets\n{len(code_blocks)} code blocks present")
        
        # Combine key elements
        extracted_text = '\n'.join(key_elements)
        
        # If still too long, truncate
        if self._estimate_tokens(extracted_text) > max_tokens:
            extracted_text = self._truncate_to_tokens(extracted_text, max_tokens)
        
        return extracted_text, {
            "method": "extract_key_info",
            "extracted_elements": len(key_elements)
        }
    
    async def _compress_summarize(
        self,
        text: str,
        max_tokens: int,
        preserve_sections: List[str]
    ) -> Tuple[str, Dict[str, Any]]:
        """Summarize text to fit within token limit."""
        # Split into sections
        sections = self._split_into_sections(text)
        
        # Summarize each section
        summarized_sections = []
        for section_title, section_content in sections:
            if any(preserve in section_title for preserve in preserve_sections):
                # Keep important sections as-is but maybe trim
                summarized_sections.append(f"## {section_title}\n{section_content}")
            else:
                # Create brief summary
                summary = self._create_section_summary(section_content)
                summarized_sections.append(f"## {section_title}\n{summary}")
        
        # Combine and check length
        summarized_text = '\n\n'.join(summarized_sections)
        
        # If still too long, apply additional truncation
        if self._estimate_tokens(summarized_text) > max_tokens:
            summarized_text = self._truncate_to_tokens(summarized_text, max_tokens)
        
        return summarized_text, {
            "method": "summarize",
            "sections_summarized": len(sections)
        }
    
    def _compress_hierarchical(
        self,
        text: str,
        max_tokens: int,
        preserve_sections: List[str]
    ) -> Tuple[str, Dict[str, Any]]:
        """Hierarchical compression maintaining structure."""
        # Extract structure
        structure = []
        
        # Level 1: Main headers
        main_sections = re.findall(r'^#\s+(.+)$', text, re.MULTILINE)
        structure.append("# Document Structure")
        structure.append('\n'.join(f"- {s}" for s in main_sections[:5]))
        
        # Level 2: Subsections (only for preserved sections)
        for preserve in preserve_sections:
            subsections = re.findall(
                rf'(?:^##\s+(.+)$).*?(?=^##|\Z)',
                text,
                re.MULTILINE | re.DOTALL
            )
            if subsections:
                structure.append(f"\n## {preserve} - Subsections")
                structure.append('\n'.join(f"  - {s}" for s in subsections[:5]))
        
        # Add summary of key points
        key_points = re.findall(r'^\s*[-*]\s+(.+)$', text, re.MULTILINE)
        if key_points:
            structure.append("\n# Key Points")
            structure.append('\n'.join(f"- {p}" for p in key_points[:10]))
        
        hierarchical_text = '\n'.join(structure)
        
        return hierarchical_text, {
            "method": "hierarchical",
            "main_sections": len(main_sections)
        }
    
    async def _compress_semantic(
        self,
        text: str,
        max_tokens: int,
        preserve_sections: List[str]
    ) -> Tuple[str, Dict[str, Any]]:
        """Semantic compression using embeddings and importance scoring."""
        # Split into sentences
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Score sentences by importance (simplified heuristic)
        scored_sentences = []
        for sentence in sentences:
            score = self._calculate_sentence_importance(sentence)
            scored_sentences.append((score, sentence))
        
        # Sort by importance
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        
        # Select top sentences up to token limit
        selected_sentences = []
        current_tokens = 0
        
        for score, sentence in scored_sentences:
            sentence_tokens = self._estimate_tokens(sentence)
            if current_tokens + sentence_tokens <= max_tokens:
                selected_sentences.append(sentence)
                current_tokens += sentence_tokens
            else:
                break
        
        # Reconstruct text (maintaining some order)
        compressed_text = '. '.join(selected_sentences) + '.'
        
        return compressed_text, {
            "method": "semantic",
            "sentences_selected": len(selected_sentences),
            "sentences_total": len(sentences)
        }
    
    def _split_into_sections(self, text: str) -> List[Tuple[str, str]]:
        """Split text into titled sections."""
        sections = []
        current_section = None
        current_content = []
        
        for line in text.split('\n'):
            # Check for section header
            header_match = re.match(r'^#+\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_section:
                    sections.append((current_section, '\n'.join(current_content)))
                
                # Start new section
                current_section = header_match.group(1)
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Save last section
        if current_section:
            sections.append((current_section, '\n'.join(current_content)))
        
        return sections
    
    def _create_section_summary(self, content: str) -> str:
        """Create a brief summary of section content."""
        # Extract key elements
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        
        # Take first few sentences and key points
        summary_parts = []
        
        # First sentence
        if lines:
            summary_parts.append(lines[0][:200])
        
        # Bullet points
        bullets = [l for l in lines if l.startswith(('-', '*'))]
        if bullets:
            summary_parts.append('\n'.join(bullets[:3]))
        
        return '\n'.join(summary_parts)
    
    def _calculate_sentence_importance(self, sentence: str) -> float:
        """Calculate importance score for a sentence."""
        score = 0.0
        
        # Length factor (not too short, not too long)
        word_count = len(sentence.split())
        if 10 <= word_count <= 30:
            score += 0.3
        
        # Contains numbers or specific data
        if re.search(r'\d+', sentence):
            score += 0.2
        
        # Contains important keywords
        important_keywords = [
            'important', 'key', 'critical', 'must', 'require',
            'essential', 'significant', 'primary', 'main'
        ]
        if any(keyword in sentence.lower() for keyword in important_keywords):
            score += 0.3
        
        # Contains action verbs
        action_verbs = [
            'implement', 'create', 'develop', 'design', 'build',
            'ensure', 'provide', 'enable', 'support'
        ]
        if any(verb in sentence.lower() for verb in action_verbs):
            score += 0.2
        
        return score
    
    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to approximately max_tokens."""
        # Rough estimate: 4 chars per token average
        max_chars = max_tokens * 4
        
        if len(text) <= max_chars:
            return text
        
        # Truncate at word boundary
        truncated = text[:max_chars]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    def _estimate_information_preservation(
        self,
        original: str,
        compressed: str
    ) -> float:
        """Estimate how much information was preserved."""
        # Simple heuristic based on character overlap
        original_words = set(original.lower().split())
        compressed_words = set(compressed.lower().split())
        
        if not original_words:
            return 1.0
        
        overlap = len(original_words & compressed_words) / len(original_words)
        return overlap
    
    def _log_compression(self, result: CompressionResult) -> None:
        """Log compression for analytics."""
        self.compression_history.append({
            "original_tokens": result.original_tokens,
            "compressed_tokens": result.compressed_tokens,
            "compression_ratio": result.compression_ratio,
            "preserved_information": result.preserved_information,
            "strategy": result.strategy_used.value
        })
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get statistics about compressions."""
        if not self.compression_history:
            return {"total_compressions": 0}
        
        avg_compression_ratio = sum(c["compression_ratio"] for c in self.compression_history) / len(self.compression_history)
        avg_preservation = sum(c["preserved_information"] for c in self.compression_history) / len(self.compression_history)
        
        strategy_counts = {}
        for comp in self.compression_history:
            strategy = comp["strategy"]
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        return {
            "total_compressions": len(self.compression_history),
            "average_compression_ratio": avg_compression_ratio,
            "average_information_preservation": avg_preservation,
            "strategy_distribution": strategy_counts
        }


# Example usage
async def example_usage():
    """Example of using the context compressor."""
    compressor = ContextCompressor()
    
    # Example long text
    long_text = """
# Project Overview
This is a comprehensive guide to building a distributed system.

## Architecture
The system consists of multiple microservices communicating via message queues.
- Service A handles authentication
- Service B processes payments
- Service C manages user data
- Service D handles notifications

## Implementation Details
Each service is containerized using Docker and deployed on Kubernetes.
The system uses Redis for caching and PostgreSQL for persistent storage.
Load balancing is handled by NGINX.

## Best Practices
1. Use circuit breakers for resilience
2. Implement proper logging and monitoring
3. Use API versioning
4. Implement rate limiting
5. Secure all endpoints with authentication
    """ * 5  # Make it longer
    
    # Compress with different strategies
    result1 = await compressor.compress(long_text, max_tokens=200, strategy=CompressionStrategy.EXTRACT_KEY_INFO)
    print(f"Strategy: {result1.strategy_used.value}")
    print(f"Compression: {result1.original_tokens} -> {result1.compressed_tokens} tokens")
    print(f"Preserved: {result1.preserved_information:.2%}\n")
    
    result2 = await compressor.compress(long_text, max_tokens=100, strategy=CompressionStrategy.HIERARCHICAL)
    print(f"Strategy: {result2.strategy_used.value}")
    print(f"Compression: {result2.original_tokens} -> {result2.compressed_tokens} tokens\n")
    
    # Print stats
    stats = compressor.get_compression_stats()
    print(f"Compression Stats: {stats}")


if __name__ == "__main__":
    asyncio.run(example_usage())
