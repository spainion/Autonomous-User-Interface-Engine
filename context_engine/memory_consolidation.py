"""
Memory Consolidation System for Context Engine.

Features:
- Automatic memory summarization
- Importance scoring
- Memory pruning
- Long-term memory formation
- Forgetting curve simulation
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import math


class MemoryImportanceScorer:
    """
    Scores memory importance based on multiple factors.
    
    Factors:
    - Recency: How recent the memory is
    - Frequency: How often accessed
    - Relevance: Connection to other memories
    - Emotional weight: Associated importance metadata
    """
    
    def __init__(
        self,
        recency_weight: float = 0.3,
        frequency_weight: float = 0.3,
        relevance_weight: float = 0.2,
        emotional_weight: float = 0.2
    ):
        """
        Initialize importance scorer.
        
        Args:
            recency_weight: Weight for recency factor
            frequency_weight: Weight for access frequency
            relevance_weight: Weight for connectivity
            emotional_weight: Weight for emotional/metadata importance
        """
        self.recency_weight = recency_weight
        self.frequency_weight = frequency_weight
        self.relevance_weight = relevance_weight
        self.emotional_weight = emotional_weight
    
    def score_memory(
        self,
        memory: Dict[str, Any],
        current_time: float,
        connection_count: int = 0
    ) -> float:
        """
        Calculate importance score for a memory.
        
        Args:
            memory: Memory object with metadata
            current_time: Current timestamp
            connection_count: Number of connections to other memories
        
        Returns:
            Importance score (0-1)
        """
        # Recency score (exponential decay)
        created_at = memory.get('created_at', current_time)
        time_diff = current_time - created_at
        recency_score = math.exp(-time_diff / 86400)  # Decay over days
        
        # Frequency score (normalized access count)
        access_count = memory.get('access_count', 1)
        frequency_score = min(1.0, access_count / 10.0)  # Normalize to 10 accesses
        
        # Relevance score (based on connections)
        relevance_score = min(1.0, connection_count / 5.0)  # Normalize to 5 connections
        
        # Emotional weight (from metadata)
        emotional_score = memory.get('importance', 0.5)
        
        # Weighted combination
        total_score = (
            self.recency_weight * recency_score +
            self.frequency_weight * frequency_score +
            self.relevance_weight * relevance_score +
            self.emotional_weight * emotional_score
        )
        
        return total_score


class MemoryConsolidation:
    """
    Memory consolidation system for long-term storage optimization.
    
    Features:
    - Automatic summarization of similar memories
    - Importance-based pruning
    - Long-term memory formation
    - Forgetting curve simulation
    - Memory replay for reinforcement
    """
    
    def __init__(
        self,
        max_memories: int = 10000,
        consolidation_threshold: int = 1000,
        importance_threshold: float = 0.3,
        similarity_threshold: float = 0.85
    ):
        """
        Initialize memory consolidation system.
        
        Args:
            max_memories: Maximum number of memories to keep
            consolidation_threshold: Trigger consolidation at this count
            importance_threshold: Minimum importance to keep
            similarity_threshold: Threshold for merging similar memories
        """
        self.max_memories = max_memories
        self.consolidation_threshold = consolidation_threshold
        self.importance_threshold = importance_threshold
        self.similarity_threshold = similarity_threshold
        
        # Importance scorer
        self.importance_scorer = MemoryImportanceScorer()
        
        # Consolidation history
        self.consolidation_history: List[Dict[str, Any]] = []
    
    def should_consolidate(self, memory_count: int) -> bool:
        """Check if consolidation should be triggered."""
        return memory_count >= self.consolidation_threshold
    
    def consolidate_memories(
        self,
        memories: List[Dict[str, Any]],
        connections: Dict[str, List[str]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Consolidate memories through importance-based pruning and summarization.
        
        Args:
            memories: List of memory objects
            connections: Graph of memory connections
        
        Returns:
            (consolidated_memories, consolidation_report)
        """
        current_time = datetime.now().timestamp()
        
        # Score all memories
        scored_memories = []
        for memory in memories:
            memory_id = memory.get('id', '')
            connection_count = len(connections.get(memory_id, []))
            
            score = self.importance_scorer.score_memory(
                memory,
                current_time,
                connection_count
            )
            
            scored_memories.append((memory, score))
        
        # Sort by importance
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        
        # Separate into keep and prune
        keep_memories = []
        prune_memories = []
        
        for memory, score in scored_memories:
            if len(keep_memories) < self.max_memories and score >= self.importance_threshold:
                keep_memories.append(memory)
            else:
                prune_memories.append(memory)
        
        # Try to summarize similar memories
        consolidated = self._summarize_similar_memories(keep_memories)
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'original_count': len(memories),
            'kept_count': len(consolidated),
            'pruned_count': len(prune_memories),
            'summarized_count': len(keep_memories) - len(consolidated),
            'avg_importance': np.mean([s for _, s in scored_memories]),
            'threshold': self.importance_threshold
        }
        
        self.consolidation_history.append(report)
        
        return consolidated, report
    
    def _summarize_similar_memories(
        self,
        memories: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Summarize similar memories into consolidated versions.
        
        Args:
            memories: List of memories
        
        Returns:
            Consolidated memories
        """
        if len(memories) < 2:
            return memories
        
        consolidated = []
        processed = set()
        
        for i, memory_i in enumerate(memories):
            if i in processed:
                continue
            
            # Find similar memories
            similar_group = [memory_i]
            similar_indices = [i]
            
            for j, memory_j in enumerate(memories[i+1:], start=i+1):
                if j in processed:
                    continue
                
                # Check similarity (simplified - would use embeddings in practice)
                similarity = self._calculate_similarity(memory_i, memory_j)
                
                if similarity >= self.similarity_threshold:
                    similar_group.append(memory_j)
                    similar_indices.append(j)
            
            # Mark as processed
            processed.update(similar_indices)
            
            # Consolidate group
            if len(similar_group) > 1:
                consolidated_memory = self._merge_memories(similar_group)
                consolidated.append(consolidated_memory)
            else:
                consolidated.append(memory_i)
        
        return consolidated
    
    def _calculate_similarity(
        self,
        memory1: Dict[str, Any],
        memory2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two memories."""
        # Simple heuristic - would use vector similarity in practice
        
        # Check content type
        if memory1.get('type') != memory2.get('type'):
            return 0.0
        
        # Check temporal proximity
        t1 = memory1.get('created_at', 0)
        t2 = memory2.get('created_at', 0)
        time_diff = abs(t1 - t2)
        
        time_similarity = math.exp(-time_diff / 3600)  # Decay over hours
        
        # Check content overlap (simplified)
        content1 = str(memory1.get('content', ''))
        content2 = str(memory2.get('content', ''))
        
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        overlap = len(words1 & words2) / max(len(words1), len(words2))
        
        return 0.5 * time_similarity + 0.5 * overlap
    
    def _merge_memories(
        self,
        memories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Merge multiple similar memories into one consolidated memory.
        
        Args:
            memories: Memories to merge
        
        Returns:
            Consolidated memory
        """
        if len(memories) == 1:
            return memories[0]
        
        # Use most recent as base
        base = max(memories, key=lambda m: m.get('created_at', 0))
        
        # Aggregate metadata
        consolidated = base.copy()
        consolidated['consolidated'] = True
        consolidated['source_count'] = len(memories)
        consolidated['source_ids'] = [m.get('id', '') for m in memories]
        
        # Sum access counts
        consolidated['access_count'] = sum(m.get('access_count', 1) for m in memories)
        
        # Average importance
        consolidated['importance'] = np.mean([m.get('importance', 0.5) for m in memories])
        
        # Keep earliest created_at
        consolidated['created_at'] = min(m.get('created_at', 0) for m in memories)
        
        return consolidated
    
    def apply_forgetting_curve(
        self,
        memories: List[Dict[str, Any]],
        half_life_days: float = 30.0
    ) -> List[Dict[str, Any]]:
        """
        Apply forgetting curve to decay memory strength over time.
        
        Based on Ebbinghaus forgetting curve.
        
        Args:
            memories: List of memories
            half_life_days: Half-life for memory decay in days
        
        Returns:
            Memories with updated strength
        """
        current_time = datetime.now().timestamp()
        
        updated_memories = []
        for memory in memories:
            memory = memory.copy()
            
            # Calculate time since last access
            last_access = memory.get('last_accessed', memory.get('created_at', current_time))
            time_diff_days = (current_time - last_access) / 86400
            
            # Calculate decay using exponential function
            decay_factor = 0.5 ** (time_diff_days / half_life_days)
            
            # Update memory strength
            original_strength = memory.get('strength', 1.0)
            memory['strength'] = original_strength * decay_factor
            
            # Only keep memories above threshold
            if memory['strength'] >= 0.1:  # 10% threshold
                updated_memories.append(memory)
        
        return updated_memories
    
    def reinforce_memory(
        self,
        memory: Dict[str, Any],
        reinforcement_strength: float = 0.1
    ) -> Dict[str, Any]:
        """
        Reinforce a memory (strengthen it).
        
        Used when a memory is accessed or deemed important.
        
        Args:
            memory: Memory to reinforce
            reinforcement_strength: Amount to strengthen (0-1)
        
        Returns:
            Reinforced memory
        """
        memory = memory.copy()
        
        # Update access time
        memory['last_accessed'] = datetime.now().timestamp()
        memory['access_count'] = memory.get('access_count', 0) + 1
        
        # Increase strength (with ceiling)
        current_strength = memory.get('strength', 0.5)
        memory['strength'] = min(1.0, current_strength + reinforcement_strength)
        
        # Increase importance slightly
        current_importance = memory.get('importance', 0.5)
        memory['importance'] = min(1.0, current_importance + reinforcement_strength * 0.5)
        
        return memory
    
    def get_consolidation_stats(self) -> Dict[str, Any]:
        """Get statistics about consolidation history."""
        if not self.consolidation_history:
            return {}
        
        return {
            'total_consolidations': len(self.consolidation_history),
            'total_memories_pruned': sum(c['pruned_count'] for c in self.consolidation_history),
            'total_memories_summarized': sum(c['summarized_count'] for c in self.consolidation_history),
            'avg_retention_rate': np.mean([
                c['kept_count'] / c['original_count']
                for c in self.consolidation_history
                if c['original_count'] > 0
            ]),
            'last_consolidation': self.consolidation_history[-1] if self.consolidation_history else None
        }
    
    def replay_memories(
        self,
        memories: List[Dict[str, Any]],
        replay_count: int = 10,
        selection_strategy: str = 'importance'
    ) -> List[Dict[str, Any]]:
        """
        Select memories for replay/rehearsal to strengthen them.
        
        Args:
            memories: Available memories
            replay_count: Number of memories to replay
            selection_strategy: 'importance', 'recent', or 'random'
        
        Returns:
            Selected memories for replay
        """
        if not memories:
            return []
        
        replay_count = min(replay_count, len(memories))
        
        if selection_strategy == 'importance':
            # Select most important
            scored = sorted(
                memories,
                key=lambda m: m.get('importance', 0),
                reverse=True
            )
            return scored[:replay_count]
        
        elif selection_strategy == 'recent':
            # Select most recent
            scored = sorted(
                memories,
                key=lambda m: m.get('last_accessed', m.get('created_at', 0)),
                reverse=True
            )
            return scored[:replay_count]
        
        elif selection_strategy == 'random':
            # Random selection
            indices = np.random.choice(len(memories), replay_count, replace=False)
            return [memories[i] for i in indices]
        
        else:
            raise ValueError(f"Unknown selection strategy: {selection_strategy}")
