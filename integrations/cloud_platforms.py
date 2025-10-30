"""
Cloud Platform Integrations for Context Engine

Provides adapters for major cloud platforms:
- AWS (S3, Lambda, SageMaker)
- Google Cloud (Cloud Storage, Cloud Functions, Vertex AI)
- Azure (Blob Storage, Azure Functions, Azure ML)
"""

from typing import Dict, Any, Optional, List
import json


class AWSAdapter:
    """AWS integration for S3 storage, Lambda functions, and SageMaker"""
    
    def __init__(self, context_engine, region_name: str = 'us-east-1'):
        self.context_engine = context_engine
        self.region_name = region_name
        self.s3 = None
        self.lambda_client = None
        self.sagemaker = None
    
    def connect_s3(self):
        """Connect to AWS S3"""
        try:
            import boto3
            self.s3 = boto3.client('s3', region_name=self.region_name)
            return True
        except ImportError:
            print("boto3 not installed. Install with: pip install boto3")
            return False
        except Exception as e:
            print(f"AWS S3 connection error: {e}")
            return False
    
    def upload_context_to_s3(self, bucket_name: str, key: str):
        """Upload context graph to S3"""
        if not self.s3:
            return False
        
        try:
            # Serialize context
            context_data = {
                'nodes': [{'id': node.id, 'content': node.content} 
                         for node in self.context_engine.nodes.values()],
                'edges': [{'source': edge.source_id, 'target': edge.target_id} 
                         for edge in self.context_engine.edges]
            }
            
            self.s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=json.dumps(context_data),
                ContentType='application/json'
            )
            return True
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return False
    
    def download_context_from_s3(self, bucket_name: str, key: str):
        """Download context graph from S3"""
        if not self.s3:
            return None
        
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=key)
            context_data = json.loads(response['Body'].read())
            return context_data
        except Exception as e:
            print(f"Error downloading from S3: {e}")
            return None
    
    def connect_lambda(self):
        """Connect to AWS Lambda"""
        try:
            import boto3
            self.lambda_client = boto3.client('lambda', region_name=self.region_name)
            return True
        except Exception as e:
            print(f"AWS Lambda connection error: {e}")
            return False
    
    def invoke_lambda(self, function_name: str, payload: Dict[str, Any]):
        """Invoke Lambda function with context data"""
        if not self.lambda_client:
            return None
        
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            return json.loads(response['Payload'].read())
        except Exception as e:
            print(f"Error invoking Lambda: {e}")
            return None


class GCPAdapter:
    """Google Cloud Platform integration"""
    
    def __init__(self, context_engine, project_id: Optional[str] = None):
        self.context_engine = context_engine
        self.project_id = project_id
        self.storage_client = None
        self.functions_client = None
    
    def connect_storage(self):
        """Connect to Google Cloud Storage"""
        try:
            from google.cloud import storage
            self.storage_client = storage.Client(project=self.project_id)
            return True
        except ImportError:
            print("google-cloud-storage not installed. Install with: pip install google-cloud-storage")
            return False
        except Exception as e:
            print(f"GCP Storage connection error: {e}")
            return False
    
    def upload_to_gcs(self, bucket_name: str, blob_name: str):
        """Upload context to Google Cloud Storage"""
        if not self.storage_client:
            return False
        
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            # Serialize context
            context_data = {
                'nodes': [{'id': node.id, 'content': node.content} 
                         for node in self.context_engine.nodes.values()],
                'edges': [{'source': edge.source_id, 'target': edge.target_id} 
                         for edge in self.context_engine.edges]
            }
            
            blob.upload_from_string(
                json.dumps(context_data),
                content_type='application/json'
            )
            return True
        except Exception as e:
            print(f"Error uploading to GCS: {e}")
            return False
    
    def download_from_gcs(self, bucket_name: str, blob_name: str):
        """Download context from Google Cloud Storage"""
        if not self.storage_client:
            return None
        
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            context_data = json.loads(blob.download_as_string())
            return context_data
        except Exception as e:
            print(f"Error downloading from GCS: {e}")
            return None


class AzureAdapter:
    """Azure integration for Blob Storage, Azure Functions, and Azure ML"""
    
    def __init__(self, context_engine, connection_string: Optional[str] = None):
        self.context_engine = context_engine
        self.connection_string = connection_string
        self.blob_service_client = None
    
    def connect_blob_storage(self):
        """Connect to Azure Blob Storage"""
        try:
            from azure.storage.blob import BlobServiceClient
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
            return True
        except ImportError:
            print("azure-storage-blob not installed. Install with: pip install azure-storage-blob")
            return False
        except Exception as e:
            print(f"Azure Blob Storage connection error: {e}")
            return False
    
    def upload_to_blob(self, container_name: str, blob_name: str):
        """Upload context to Azure Blob Storage"""
        if not self.blob_service_client:
            return False
        
        try:
            # Serialize context
            context_data = {
                'nodes': [{'id': node.id, 'content': node.content} 
                         for node in self.context_engine.nodes.values()],
                'edges': [{'source': edge.source_id, 'target': edge.target_id} 
                         for edge in self.context_engine.edges]
            }
            
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name
            )
            blob_client.upload_blob(
                json.dumps(context_data),
                overwrite=True
            )
            return True
        except Exception as e:
            print(f"Error uploading to Azure Blob: {e}")
            return False
    
    def download_from_blob(self, container_name: str, blob_name: str):
        """Download context from Azure Blob Storage"""
        if not self.blob_service_client:
            return None
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name
            )
            blob_data = blob_client.download_blob().readall()
            context_data = json.loads(blob_data)
            return context_data
        except Exception as e:
            print(f"Error downloading from Azure Blob: {e}")
            return None


class MultiCloudAdapter:
    """Multi-cloud adapter for working with multiple cloud providers"""
    
    def __init__(self, context_engine):
        self.context_engine = context_engine
        self.aws = AWSAdapter(context_engine)
        self.gcp = GCPAdapter(context_engine)
        self.azure = AzureAdapter(context_engine)
    
    def sync_to_cloud(self, provider: str, **kwargs):
        """Sync context to specified cloud provider"""
        if provider == 'aws':
            return self.aws.upload_context_to_s3(**kwargs)
        elif provider == 'gcp':
            return self.gcp.upload_to_gcs(**kwargs)
        elif provider == 'azure':
            return self.azure.upload_to_blob(**kwargs)
        else:
            print(f"Unknown provider: {provider}")
            return False
    
    def load_from_cloud(self, provider: str, **kwargs):
        """Load context from specified cloud provider"""
        if provider == 'aws':
            return self.aws.download_context_from_s3(**kwargs)
        elif provider == 'gcp':
            return self.gcp.download_from_gcs(**kwargs)
        elif provider == 'azure':
            return self.azure.download_from_blob(**kwargs)
        else:
            print(f"Unknown provider: {provider}")
            return None
