"""
Webhook Management for Autonomous UI Engine
Phase 6: Innovation - Integrations

Webhook registration and event delivery.
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import hashlib
import hmac

logger = logging.getLogger(__name__)


class WebhookEvent(Enum):
    """Webhook event types."""
    UI_GENERATED = "ui.generated"
    UI_UPDATED = "ui.updated"
    UI_DELETED = "ui.deleted"
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    PLUGIN_LOADED = "plugin.loaded"
    ERROR_OCCURRED = "error.occurred"


@dataclass
class Webhook:
    """Represents a webhook registration."""
    id: str
    url: str
    events: List[str]
    secret: Optional[str] = None
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WebhookDelivery:
    """Represents a webhook delivery attempt."""
    webhook_id: str
    event: str
    payload: Dict[str, Any]
    status_code: Optional[int] = None
    success: bool = False
    error: Optional[str] = None
    attempts: int = 0


class WebhookManager:
    """
    Manages webhook registrations and deliveries.
    """
    
    def __init__(self):
        """Initialize webhook manager."""
        self._webhooks: Dict[str, Webhook] = {}
        self._deliveries: List[WebhookDelivery] = []
        self._max_retries = 3
        
    def register_webhook(
        self,
        url: str,
        events: List[str],
        secret: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register a new webhook.
        
        Args:
            url: Webhook URL
            events: List of events to subscribe to
            secret: Optional secret for signature verification
            metadata: Optional metadata
            
        Returns:
            Webhook ID
        """
        webhook_id = hashlib.sha256(f"{url}{events}".encode()).hexdigest()[:16]
        
        webhook = Webhook(
            id=webhook_id,
            url=url,
            events=events,
            secret=secret,
            metadata=metadata or {}
        )
        
        self._webhooks[webhook_id] = webhook
        logger.info(f"Registered webhook: {webhook_id} for events {events}")
        
        return webhook_id
    
    def unregister_webhook(self, webhook_id: str) -> bool:
        """
        Unregister a webhook.
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            True if successful
        """
        if webhook_id in self._webhooks:
            del self._webhooks[webhook_id]
            logger.info(f"Unregistered webhook: {webhook_id}")
            return True
        return False
    
    async def trigger_event(
        self,
        event: str,
        payload: Dict[str, Any]
    ) -> List[WebhookDelivery]:
        """
        Trigger an event and deliver to registered webhooks.
        
        Args:
            event: Event name
            payload: Event payload
            
        Returns:
            List of delivery results
        """
        logger.info(f"Triggering webhook event: {event}")
        
        # Find webhooks subscribed to this event
        webhooks = [
            w for w in self._webhooks.values()
            if event in w.events and w.active
        ]
        
        if not webhooks:
            logger.debug(f"No webhooks registered for event: {event}")
            return []
        
        # Deliver to all webhooks
        deliveries = []
        for webhook in webhooks:
            delivery = await self._deliver_webhook(webhook, event, payload)
            deliveries.append(delivery)
            self._deliveries.append(delivery)
        
        return deliveries
    
    async def _deliver_webhook(
        self,
        webhook: Webhook,
        event: str,
        payload: Dict[str, Any]
    ) -> WebhookDelivery:
        """
        Deliver webhook with retries.
        
        Args:
            webhook: Webhook to deliver to
            event: Event name
            payload: Event payload
            
        Returns:
            Delivery result
        """
        delivery = WebhookDelivery(
            webhook_id=webhook.id,
            event=event,
            payload=payload
        )
        
        for attempt in range(self._max_retries):
            delivery.attempts = attempt + 1
            
            try:
                # Prepare payload
                webhook_payload = {
                    "event": event,
                    "timestamp": "2024-01-01T00:00:00Z",
                    "data": payload
                }
                
                # Add signature if secret is provided
                if webhook.secret:
                    signature = self._generate_signature(webhook_payload, webhook.secret)
                    webhook_payload["signature"] = signature
                
                # In production, actually send HTTP POST request
                # async with aiohttp.ClientSession() as session:
                #     async with session.post(webhook.url, json=webhook_payload) as resp:
                #         delivery.status_code = resp.status
                #         delivery.success = resp.status == 200
                
                # Simulated delivery
                delivery.status_code = 200
                delivery.success = True
                
                logger.info(
                    f"Webhook delivered: {webhook.id} "
                    f"(attempt {attempt + 1}/{self._max_retries})"
                )
                break
                
            except Exception as e:
                delivery.error = str(e)
                logger.error(f"Webhook delivery failed: {e}")
                
                if attempt < self._max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return delivery
    
    def _generate_signature(
        self,
        payload: Dict[str, Any],
        secret: str
    ) -> str:
        """
        Generate HMAC signature for payload.
        
        Args:
            payload: Payload to sign
            secret: Secret key
            
        Returns:
            Signature string
        """
        import json
        payload_str = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def verify_signature(
        self,
        payload: Dict[str, Any],
        signature: str,
        secret: str
    ) -> bool:
        """
        Verify webhook signature.
        
        Args:
            payload: Received payload
            signature: Received signature
            secret: Secret key
            
        Returns:
            True if signature is valid
        """
        expected_signature = self._generate_signature(payload, secret)
        return hmac.compare_digest(signature, expected_signature)
    
    def list_webhooks(self, event: Optional[str] = None) -> List[Webhook]:
        """
        List registered webhooks.
        
        Args:
            event: Optional event filter
            
        Returns:
            List of webhooks
        """
        webhooks = list(self._webhooks.values())
        
        if event:
            webhooks = [w for w in webhooks if event in w.events]
        
        return webhooks
    
    def get_webhook_stats(self) -> Dict[str, Any]:
        """
        Get webhook statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_webhooks = len(self._webhooks)
        active_webhooks = sum(1 for w in self._webhooks.values() if w.active)
        total_deliveries = len(self._deliveries)
        successful_deliveries = sum(1 for d in self._deliveries if d.success)
        
        return {
            "total_webhooks": total_webhooks,
            "active_webhooks": active_webhooks,
            "total_deliveries": total_deliveries,
            "successful_deliveries": successful_deliveries,
            "success_rate": successful_deliveries / total_deliveries if total_deliveries > 0 else 0.0
        }


# Example usage
async def example_usage():
    """Example of using webhook manager."""
    manager = WebhookManager()
    
    # Register webhook
    webhook_id = manager.register_webhook(
        url="https://example.com/webhook",
        events=["ui.generated", "ui.updated"],
        secret="my-secret-key"
    )
    print(f"Registered webhook: {webhook_id}")
    
    # Trigger event
    deliveries = await manager.trigger_event(
        "ui.generated",
        {"ui_name": "dashboard", "url": "https://example.com/dashboard"}
    )
    print(f"Delivered to {len(deliveries)} webhooks")
    
    # Get stats
    stats = manager.get_webhook_stats()
    print(f"Stats: {stats}")


if __name__ == "__main__":
    asyncio.run(example_usage())
