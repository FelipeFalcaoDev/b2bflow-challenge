"""
Z-API client module for b2bflow-challenge.

Handles WhatsApp message sending via Z-API.
Single responsibility: send messages only.
"""

import logging
from typing import List

import requests

from src.config import Config

logger = logging.getLogger(__name__)

# Message template from client requirements
MESSAGE_TEMPLATE = "Olá, {name} tudo bem com você?"

class WhatsAppSender:
    """
    Sends WhatsApp messages via Z-API.

    Applies SRP: only handles message delivery, not contact fetching
    or configuration management.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize Z-API client.

        Args:
            config: Config instance with Z-API URL.

        Raises:
            ValueError: If URL is invalid.
        """
        # Z-API URL already includes instance ID and token
        # No separate Authorization header needed
        self.url: str = config.zapi_url
        self.headers: dict = {"Content-Type": "application/json"}
        logger.info("✓ Z-API client initialized")

    def send_message(self, phone_number: str, message: str) -> bool:
        """
        Send WhatsApp message to a phone number.

        Args:
            phone_number: WhatsApp number in international format (e.g., 5585988776655).
            message: Message content to send.

        Returns:
            True if sent successfully, False otherwise.
        """
        try:
            logger.info(f"Sending message to {phone_number}...")

            payload = {
                "phone": phone_number,
                "message": message,
            }

            # 10s timeout: Z-API typically responds in 2-3s
            # Higher timeout accounts for network latency
            response = requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                timeout=10,
            )

            if 200 <= response.status_code < 300:
                logger.info(f"✓ Message sent successfully to {phone_number}")
                return True
            else:
                logger.error(
                    f"✗ Failed to send to {phone_number}. "
                    f"Status: {response.status_code}. "
                    f"Response: {response.text}"
                )
                return False

        except requests.exceptions.Timeout:
            logger.error(f"✗ Timeout sending to {phone_number}")
            return False
        except requests.exceptions.RequestException as error:
            logger.error(f"✗ Network error sending to {phone_number}: {error}")
            return False
        except Exception as error:
            logger.error(f"✗ Unexpected error sending to {phone_number}: {error}")
            return False


def send_messages(config: Config, contacts: List[dict]) -> dict:
    """
    Send messages to multiple contacts.

    Args:
        config: Config instance with Z-API credentials.
        contacts: List of contacts with 'name' and 'phone' fields.

    Returns:
        Dictionary with send statistics:
        {
            "sent": 2,
            "failed": 1,
            "total": 3
        }
    """
    logger.info(f"Starting message sending for {len(contacts)} contact(s)...")

    sender = WhatsAppSender(config)

    counters = {
        "sent": 0,
        "failed": 0,
        "total": len(contacts),
    }

    for contact in contacts:
        name = contact.get("name", "User")
        phone = contact.get("phone", "")

        message = MESSAGE_TEMPLATE.format(name=name)
        success = sender.send_message(phone, message)

        if success:
            counters["sent"] += 1
        else:
            counters["failed"] += 1

    logger.info(
        f"✓ Sending completed: {counters['sent']} sent, "
        f"{counters['failed']} failed"
    )

    return counters