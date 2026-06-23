"""
Main entry point for b2bflow-challenge.

Orchestrates the complete workflow: config → fetch → send.
"""

import logging
import sys

from src.config import load_config
from src.supabase_client import fetch_contacts
from src.whatsapp_sender import send_messages

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def main() -> int:
    """
    Orchestrate the complete message sending workflow.

    Flow:
    1. Load configuration from .env
    2. Fetch contacts from Supabase
    3. Send WhatsApp messages to each contact
    4. Return exit code based on success/failure

    Returns:
        0 if at least one message sent successfully, 1 on error.
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting b2bflow WhatsApp Message Sender")
        logger.info("=" * 60)

        # Load configuration
        logger.info("Step 1: Loading configuration...")
        config = load_config()
        logger.info("✓ Configuration loaded successfully")

        # Fetch contacts from database
        logger.info("Step 2: Fetching contacts from Supabase...")
        contacts = fetch_contacts(config, limit=3)

        if not contacts:
            logger.error("✗ No contacts found. Aborting execution.")
            return 1

        logger.info(f"✓ Found {len(contacts)} contact(s)")

        # Send messages
        logger.info("Step 3: Sending WhatsApp messages...")
        results = send_messages(config, contacts)

        # Summary
        logger.info("=" * 60)
        logger.info("Final Summary:")
        logger.info(f"  Total contacts: {results['total']}")
        logger.info(f"  Successfully sent: {results['sent']}")
        logger.info(f"  Failed: {results['failed']}")
        logger.info("=" * 60)

        if results["sent"] > 0:
            logger.info("✓ Process completed successfully!")
            return 0
        else:
            logger.error("✗ No messages were sent. Check logs above.")
            return 1

    except ValueError as error:
        logger.error(f"✗ Configuration Error: {error}")
        return 1

    except Exception as error:
        logger.error(f"✗ Unexpected Error: {error}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)