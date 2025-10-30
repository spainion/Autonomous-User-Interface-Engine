"""
Database Integrations for Context Engine

Provides adapters for popular databases:
- PostgreSQL (with pgvector for vector storage)
- MongoDB
- Redis
- SQLite
- Elasticsearch
"""

from typing import List, Dict, Any, Optional
import json


class PostgreSQLAdapter:
    """PostgreSQL adapter with pgvector support for efficient vector storage"""
    
    def __init__(self, context_engine, connection_string: Optional[str] = None):
        self.context_engine = context_engine
        self.connection_string = connection_string
        self.conn = None
    
    def connect(self):
        """Connect to PostgreSQL"""
        try:
            import psycopg2
            self.conn = psycopg2.connect(self.connection_string)
            return True
        except ImportError:
            print("psycopg2 not installed. Install with: pip install psycopg2-binary")
            return False
        except Exception as e:
            print(f"PostgreSQL connection error: {e}")
            return False
    
    def create_vector_table(self):
        """Create table with pgvector extension"""
        if not self.conn:
            return False
        
        try:
            with self.conn.cursor() as cur:
                # Enable pgvector extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                
                # Create table for nodes with vector embeddings
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS context_nodes (
                        id TEXT PRIMARY KEY,
                        content TEXT,
                        embedding vector(384),
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)
                
                # Create index for fast vector similarity search
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_embedding 
                    ON context_nodes USING ivfflat (embedding vector_cosine_ops)
                """)
                
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating vector table: {e}")
            return False
    
    def store_nodes(self, nodes: List[Any]):
        """Store nodes in PostgreSQL"""
        if not self.conn:
            return False
        
        try:
            with self.conn.cursor() as cur:
                for node in nodes:
                    cur.execute("""
                        INSERT INTO context_nodes (id, content, embedding, metadata)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                            content = EXCLUDED.content,
                            embedding = EXCLUDED.embedding,
                            metadata = EXCLUDED.metadata
                    """, (
                        node.id,
                        node.content,
                        node.embedding.tolist() if hasattr(node, 'embedding') else None,
                        json.dumps(node.metadata if hasattr(node, 'metadata') else {})
                    ))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Error storing nodes: {e}")
            return False
    
    def vector_search(self, query_vector: List[float], k: int = 10):
        """Search for similar vectors using pgvector"""
        if not self.conn:
            return []
        
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT id, content, metadata, embedding <=> %s::vector AS distance
                    FROM context_nodes
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """, (query_vector, query_vector, k))
                return cur.fetchall()
        except Exception as e:
            print(f"Error in vector search: {e}")
            return []


class MongoDBAdapter:
    """MongoDB adapter for document storage"""
    
    def __init__(self, context_engine, connection_string: Optional[str] = None):
        self.context_engine = context_engine
        self.connection_string = connection_string
        self.client = None
        self.db = None
    
    def connect(self, database: str = "context_engine"):
        """Connect to MongoDB"""
        try:
            from pymongo import MongoClient
            self.client = MongoClient(self.connection_string)
            self.db = self.client[database]
            return True
        except ImportError:
            print("pymongo not installed. Install with: pip install pymongo")
            return False
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            return False
    
    def store_nodes(self, nodes: List[Any]):
        """Store nodes as MongoDB documents"""
        if not self.db:
            return False
        
        try:
            nodes_collection = self.db['nodes']
            for node in nodes:
                doc = {
                    '_id': node.id,
                    'content': node.content,
                    'embedding': node.embedding.tolist() if hasattr(node, 'embedding') else None,
                    'metadata': node.metadata if hasattr(node, 'metadata') else {},
                }
                nodes_collection.update_one(
                    {'_id': node.id},
                    {'$set': doc},
                    upsert=True
                )
            return True
        except Exception as e:
            print(f"Error storing nodes: {e}")
            return False


class RedisAdapter:
    """Redis adapter for high-speed caching"""
    
    def __init__(self, context_engine, host: str = 'localhost', port: int = 6379):
        self.context_engine = context_engine
        self.host = host
        self.port = port
        self.redis = None
    
    def connect(self):
        """Connect to Redis"""
        try:
            import redis
            self.redis = redis.Redis(host=self.host, port=self.port, decode_responses=True)
            return self.redis.ping()
        except ImportError:
            print("redis not installed. Install with: pip install redis")
            return False
        except Exception as e:
            print(f"Redis connection error: {e}")
            return False
    
    def cache_node(self, node_id: str, node_data: Dict[str, Any], ttl: int = 3600):
        """Cache node data in Redis"""
        if not self.redis:
            return False
        
        try:
            self.redis.setex(
                f"node:{node_id}",
                ttl,
                json.dumps(node_data)
            )
            return True
        except Exception as e:
            print(f"Error caching node: {e}")
            return False
    
    def get_cached_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached node data"""
        if not self.redis:
            return None
        
        try:
            data = self.redis.get(f"node:{node_id}")
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Error retrieving cached node: {e}")
            return None


class SQLiteAdapter:
    """SQLite adapter for lightweight embedded database"""
    
    def __init__(self, context_engine, db_path: str = "context_engine.db"):
        self.context_engine = context_engine
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to SQLite database"""
        try:
            import sqlite3
            self.conn = sqlite3.connect(self.db_path)
            self.create_tables()
            return True
        except Exception as e:
            print(f"SQLite connection error: {e}")
            return False
    
    def create_tables(self):
        """Create SQLite tables"""
        if not self.conn:
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    content TEXT,
                    embedding TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating tables: {e}")
            return False


class ElasticsearchAdapter:
    """Elasticsearch adapter for full-text search"""
    
    def __init__(self, context_engine, hosts: List[str] = None):
        self.context_engine = context_engine
        self.hosts = hosts or ['localhost:9200']
        self.es = None
    
    def connect(self):
        """Connect to Elasticsearch"""
        try:
            from elasticsearch import Elasticsearch
            self.es = Elasticsearch(self.hosts)
            return self.es.ping()
        except ImportError:
            print("elasticsearch not installed. Install with: pip install elasticsearch")
            return False
        except Exception as e:
            print(f"Elasticsearch connection error: {e}")
            return False
    
    def index_nodes(self, nodes: List[Any], index_name: str = "context_nodes"):
        """Index nodes in Elasticsearch"""
        if not self.es:
            return False
        
        try:
            for node in nodes:
                doc = {
                    'content': node.content,
                    'embedding': node.embedding.tolist() if hasattr(node, 'embedding') else None,
                    'metadata': node.metadata if hasattr(node, 'metadata') else {},
                }
                self.es.index(index=index_name, id=node.id, document=doc)
            return True
        except Exception as e:
            print(f"Error indexing nodes: {e}")
            return False
    
    def search(self, query: str, index_name: str = "context_nodes", size: int = 10):
        """Full-text search in Elasticsearch"""
        if not self.es:
            return []
        
        try:
            result = self.es.search(
                index=index_name,
                body={
                    "query": {
                        "match": {
                            "content": query
                        }
                    },
                    "size": size
                }
            )
            return result['hits']['hits']
        except Exception as e:
            print(f"Error searching: {e}")
            return []
