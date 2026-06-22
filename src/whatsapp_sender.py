import logging
from typing import List
import requests
from src.config import Config

logger = logging.getLogger(__name__)

class WhatsAppSender:
    def __init__(self, config: Config) -> None:
        self.url: str = config.zapi_url
        self.token: str = config.zapi_token
        self.headers: dict = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        logger.info("✓ Z-API client initialized")

    def send_message(self, phone_number: str, message: str) -> bool:
        try:
            logger.info(f"Sending message to {phone_number}...")
            payload = {
                "phone": phone_number,
                "message": message,
            }
            response = requests.post(
                f"{self.url}/send-message",
                json=payload,
                headers=self.headers,
                timeout=10,
            )

            if 200 <= response.status_code < 300:
                logger.info(f"✓ Message sent successfully to {phone_number}")
                return True
            
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
        message = f"Olá, {name} tudo bem com você?"

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