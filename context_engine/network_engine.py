"""
Network-Enhanced Context Engine with API integration.

Provides:
- Real-time embedding generation via APIs
- External knowledge base integration
- Collaborative filtering with remote services
- Cloud-based vector storage options
"""

from typing import Optional, List, Dict, Any
import os
import requests
import json
from context_engine import ContextEngine
from context_engine.embedding_generator import EmbeddingGenerator


class NetworkContextEngine(ContextEngine):
    """
    Enhanced Context Engine with network capabilities.
    
    Features:
    - Real-time API integration
    - Remote embedding services
    - External knowledge bases
    - Cloud synchronization
    """
    
    def __init__(
        self,
        use_openai: bool = True,
        use_openrouter: bool = True,
        whitelist_all_domains: bool = True
    ):
        """
        Initialize network-enhanced context engine.
        
        Args:
            use_openai: Use OpenAI API for embeddings
            use_openrouter: Use OpenRouter for LLM calls
            whitelist_all_domains: Allow all network access
        """
        super().__init__()
        
        self.use_openai = use_openai
        self.use_openrouter = use_openrouter
        self.whitelist_all_domains = whitelist_all_domains
        
        # Initialize embedding generator with network access
        if use_openai:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                try:
                    self.embedding_gen = EmbeddingGenerator(
                        backend="openai",
                        model="text-embedding-3-small",
                        api_key=api_key
                    )
                    self.has_embeddings = True
                except Exception as e:
                    print(f"Warning: OpenAI embeddings unavailable: {e}")
                    self.has_embeddings = False
            else:
                print("Warning: OPENAI_API_KEY not set, using fallback")
                self.has_embeddings = False
        else:
            self.has_embeddings = False
        
        # OpenRouter configuration
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_base = "https://openrouter.ai/api/v1"
    
    def add_node_with_text(
        self,
        content: Any,
        text_for_embedding: Optional[str] = None,
        **kwargs
    ) -> Any:
        """
        Add node with automatic embedding generation via API.
        
        Args:
            content: Content to store
            text_for_embedding: Text to generate embedding from
            **kwargs: Additional node parameters
        
        Returns:
            Created node
        """
        embedding = None
        
        if self.has_embeddings and text_for_embedding:
            try:
                embedding = self.embedding_gen.generate_embedding(text_for_embedding)
            except Exception as e:
                print(f"Warning: Embedding generation failed: {e}")
        
        return self.add_node(content=content, embedding=embedding, **kwargs)
    
    def enrich_from_external_api(
        self,
        node_id: str,
        api_url: str,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Enrich a node with data from external API.
        
        Args:
            node_id: Node to enrich
            api_url: External API endpoint
            api_key: Optional API key
        
        Returns:
            Enriched data from API
        """
        if not self.whitelist_all_domains:
            raise PermissionError("Network access not enabled")
        
        node = self.get_node(node_id)
        if not node:
            raise ValueError(f"Node {node_id} not found")
        
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            enriched_data = response.json()
            
            # Update node metadata
            node.metadata['enriched'] = True
            node.metadata['enriched_from'] = api_url
            node.metadata['enriched_data'] = enriched_data
            
            return enriched_data
            
        except requests.RequestException as e:
            print(f"Warning: API enrichment failed: {e}")
            return {}
    
    def query_llm(
        self,
        prompt: str,
        model: str = "openai/gpt-4-turbo",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Query LLM via OpenRouter with context awareness.
        
        Args:
            prompt: Prompt to send
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens
        
        Returns:
            LLM response
        """
        if not self.use_openrouter or not self.openrouter_key:
            return "OpenRouter not configured"
        
        if not self.whitelist_all_domains:
            raise PermissionError("Network access not enabled")
        
        url = f"{self.openrouter_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.RequestException as e:
            return f"Error: {e}"
    
    def batch_enrich_nodes(
        self,
        node_ids: List[str],
        enrichment_func: callable
    ) -> Dict[str, Any]:
        """
        Batch process multiple nodes with enrichment.
        
        Args:
            node_ids: List of node IDs to enrich
            enrichment_func: Function to enrich each node
        
        Returns:
            Dictionary of results
        """
        results = {}
        
        for node_id in node_ids:
            try:
                result = enrichment_func(node_id)
                results[node_id] = {"success": True, "data": result}
            except Exception as e:
                results[node_id] = {"success": False, "error": str(e)}
        
        return results
    
    def sync_to_cloud(
        self,
        cloud_url: str,
        api_key: str
    ) -> bool:
        """
        Synchronize context to cloud storage.
        
        Args:
            cloud_url: Cloud storage endpoint
            api_key: API key for authentication
        
        Returns:
            Success status
        """
        if not self.whitelist_all_domains:
            raise PermissionError("Network access not enabled")
        
        export_data = self.export_to_dict()
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                cloud_url,
                headers=headers,
                json=export_data,
                timeout=30
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Cloud sync failed: {e}")
            return False
    
    def load_from_cloud(
        self,
        cloud_url: str,
        api_key: str
    ) -> bool:
        """
        Load context from cloud storage.
        
        Args:
            cloud_url: Cloud storage endpoint
            api_key: API key for authentication
        
        Returns:
            Success status
        """
        if not self.whitelist_all_domains:
            raise PermissionError("Network access not enabled")
        
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(cloud_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            loaded_engine = ContextEngine.import_from_dict(data)
            
            # Copy loaded data to self
            self.nodes = loaded_engine.nodes
            self.graph = loaded_engine.graph
            self.content_hashes = loaded_engine.content_hashes
            self._update_vector_space()
            
            return True
        except requests.RequestException as e:
            print(f"Cloud load failed: {e}")
            return False
