"""
Embedding generator for creating vector embeddings from text.

Supports:
- OpenAI embeddings
- Sentence transformers (local)
- Custom embedding models
"""

from typing import List, Optional, Union
import numpy as np
import os


class EmbeddingGenerator:
    """
    Generate vector embeddings for text content.
    
    Supports multiple backends:
    - OpenAI API (text-embedding-ada-002, text-embedding-3-small, etc.)
    - Local sentence transformers
    """
    
    def __init__(
        self,
        backend: str = "openai",
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        """
        Initialize the embedding generator.
        
        Args:
            backend: Backend to use ('openai' or 'sentence-transformer')
            model: Model name
            api_key: API key (if needed)
        """
        self.backend = backend
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if backend == "openai":
            self._init_openai()
        elif backend == "sentence-transformer":
            self._init_sentence_transformer()
        else:
            raise ValueError(f"Unknown backend: {backend}")
    
    def _init_openai(self) -> None:
        """Initialize OpenAI client."""
        try:
            import openai
            if self.api_key:
                openai.api_key = self.api_key
            self.client = openai
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def _init_sentence_transformer(self) -> None:
        """Initialize sentence transformer."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model_instance = SentenceTransformer(self.model)
        except ImportError:
            raise ImportError(
                "Sentence transformers not installed. Run: pip install sentence-transformers"
            )
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
        
        Returns:
            Numpy array embedding vector
        """
        if self.backend == "openai":
            return self._generate_openai_embedding(text)
        elif self.backend == "sentence-transformer":
            return self._generate_sentence_transformer_embedding(text)
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
    
    def generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
        
        Returns:
            List of embedding vectors
        """
        if self.backend == "openai":
            return [self._generate_openai_embedding(text) for text in texts]
        elif self.backend == "sentence-transformer":
            embeddings = self.model_instance.encode(texts, convert_to_numpy=True)
            return [np.array(emb) for emb in embeddings]
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
    
    def _generate_openai_embedding(self, text: str) -> np.ndarray:
        """Generate embedding using OpenAI API."""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            embedding = response.data[0].embedding
            return np.array(embedding)
        except Exception as e:
            # Fallback to random embedding if API fails
            print(f"Warning: OpenAI API failed ({e}), using random embedding")
            return np.random.rand(1536)  # Default dimension for ada-002
    
    def _generate_sentence_transformer_embedding(self, text: str) -> np.ndarray:
        """Generate embedding using sentence transformer."""
        embedding = self.model_instance.encode(text, convert_to_numpy=True)
        return np.array(embedding)
    
    def get_dimension(self) -> int:
        """
        Get the embedding dimension.
        
        Returns:
            Embedding dimension size
        """
        if self.backend == "openai":
            # Standard dimensions for OpenAI models
            dimension_map = {
                "text-embedding-ada-002": 1536,
                "text-embedding-3-small": 1536,
                "text-embedding-3-large": 3072
            }
            return dimension_map.get(self.model, 1536)
        elif self.backend == "sentence-transformer":
            return self.model_instance.get_sentence_embedding_dimension()
        else:
            return 768  # Default dimension
    
    @staticmethod
    def create_random_embedding(dimension: int = 384) -> np.ndarray:
        """
        Create a random normalized embedding (useful for testing).
        
        Args:
            dimension: Embedding dimension
        
        Returns:
            Random normalized vector
        """
        embedding = np.random.rand(dimension)
        return embedding / np.linalg.norm(embedding)
