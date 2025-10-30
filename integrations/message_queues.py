"""
Message Queue Integrations for Context Engine

Provides adapters for message queuing systems:
- RabbitMQ
- Apache Kafka
- Redis Pub/Sub
- AWS SQS
"""

from typing import Callable, Optional, Dict, Any
import json


class RabbitMQAdapter:
    """RabbitMQ adapter for event-driven context updates"""
    
    def __init__(self, context_engine, host: str = 'localhost', port: int = 5672):
        self.context_engine = context_engine
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None
    
    def connect(self, username: str = 'guest', password: str = 'guest'):
        """Connect to RabbitMQ"""
        try:
            import pika
            credentials = pika.PlainCredentials(username, password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            return True
        except ImportError:
            print("pika not installed. Install with: pip install pika")
            return False
        except Exception as e:
            print(f"RabbitMQ connection error: {e}")
            return False
    
    def declare_queue(self, queue_name: str = 'context_updates'):
        """Declare a queue"""
        if not self.channel:
            return False
        
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            return True
        except Exception as e:
            print(f"Error declaring queue: {e}")
            return False
    
    def publish_context_update(self, queue_name: str, update_data: Dict[str, Any]):
        """Publish a context update to the queue"""
        if not self.channel:
            return False
        
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(update_data),
                properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
            )
            return True
        except Exception as e:
            print(f"Error publishing message: {e}")
            return False
    
    def consume_context_updates(self, queue_name: str, callback: Callable):
        """Consume context updates from the queue"""
        if not self.channel:
            return False
        
        def on_message(ch, method, properties, body):
            try:
                update_data = json.loads(body)
                callback(update_data)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"Error processing message: {e}")
        
        try:
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=on_message
            )
            self.channel.start_consuming()
        except Exception as e:
            print(f"Error consuming messages: {e}")
            return False


class KafkaAdapter:
    """Apache Kafka adapter for streaming context changes"""
    
    def __init__(self, context_engine, bootstrap_servers: str = 'localhost:9092'):
        self.context_engine = context_engine
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumer = None
    
    def create_producer(self):
        """Create Kafka producer"""
        try:
            from kafka import KafkaProducer
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            return True
        except ImportError:
            print("kafka-python not installed. Install with: pip install kafka-python")
            return False
        except Exception as e:
            print(f"Kafka producer error: {e}")
            return False
    
    def create_consumer(self, topic: str, group_id: str = 'context_engine'):
        """Create Kafka consumer"""
        try:
            from kafka import KafkaConsumer
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            return True
        except ImportError:
            print("kafka-python not installed. Install with: pip install kafka-python")
            return False
        except Exception as e:
            print(f"Kafka consumer error: {e}")
            return False
    
    def send_context_update(self, topic: str, update_data: Dict[str, Any]):
        """Send context update to Kafka topic"""
        if not self.producer:
            return False
        
        try:
            future = self.producer.send(topic, value=update_data)
            future.get(timeout=10)  # Wait for send to complete
            return True
        except Exception as e:
            print(f"Error sending to Kafka: {e}")
            return False
    
    def consume_context_updates(self, callback: Callable):
        """Consume context updates from Kafka"""
        if not self.consumer:
            return False
        
        try:
            for message in self.consumer:
                callback(message.value)
        except Exception as e:
            print(f"Error consuming from Kafka: {e}")
            return False


class RedisPubSubAdapter:
    """Redis Pub/Sub adapter for real-time agent coordination"""
    
    def __init__(self, context_engine, host: str = 'localhost', port: int = 6379):
        self.context_engine = context_engine
        self.host = host
        self.port = port
        self.redis = None
        self.pubsub = None
    
    def connect(self):
        """Connect to Redis"""
        try:
            import redis
            self.redis = redis.Redis(host=self.host, port=self.port, decode_responses=True)
            self.pubsub = self.redis.pubsub()
            return self.redis.ping()
        except ImportError:
            print("redis not installed. Install with: pip install redis")
            return False
        except Exception as e:
            print(f"Redis connection error: {e}")
            return False
    
    def subscribe(self, channel: str):
        """Subscribe to a channel"""
        if not self.pubsub:
            return False
        
        try:
            self.pubsub.subscribe(channel)
            return True
        except Exception as e:
            print(f"Error subscribing: {e}")
            return False
    
    def publish(self, channel: str, message: Dict[str, Any]):
        """Publish message to channel"""
        if not self.redis:
            return False
        
        try:
            self.redis.publish(channel, json.dumps(message))
            return True
        except Exception as e:
            print(f"Error publishing: {e}")
            return False
    
    def listen(self, callback: Callable):
        """Listen for messages"""
        if not self.pubsub:
            return False
        
        try:
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    callback(data)
        except Exception as e:
            print(f"Error listening: {e}")
            return False


class AWSSQSAdapter:
    """AWS SQS adapter for cloud-native queue integration"""
    
    def __init__(self, context_engine, region_name: str = 'us-east-1'):
        self.context_engine = context_engine
        self.region_name = region_name
        self.sqs = None
        self.queue_url = None
    
    def connect(self, queue_name: str):
        """Connect to AWS SQS"""
        try:
            import boto3
            self.sqs = boto3.client('sqs', region_name=self.region_name)
            response = self.sqs.get_queue_url(QueueName=queue_name)
            self.queue_url = response['QueueUrl']
            return True
        except ImportError:
            print("boto3 not installed. Install with: pip install boto3")
            return False
        except Exception as e:
            print(f"AWS SQS connection error: {e}")
            return False
    
    def send_message(self, message_body: Dict[str, Any]):
        """Send message to SQS queue"""
        if not self.sqs or not self.queue_url:
            return False
        
        try:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message_body)
            )
            return response.get('MessageId') is not None
        except Exception as e:
            print(f"Error sending SQS message: {e}")
            return False
    
    def receive_messages(self, max_messages: int = 10, wait_time: int = 20):
        """Receive messages from SQS queue"""
        if not self.sqs or not self.queue_url:
            return []
        
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time
            )
            return response.get('Messages', [])
        except Exception as e:
            print(f"Error receiving SQS messages: {e}")
            return []
    
    def delete_message(self, receipt_handle: str):
        """Delete message from queue after processing"""
        if not self.sqs or not self.queue_url:
            return False
        
        try:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            return True
        except Exception as e:
            print(f"Error deleting SQS message: {e}")
            return False
