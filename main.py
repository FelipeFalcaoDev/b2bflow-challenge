"""Main module for b2bflow-challenge."""
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
    """Main function orchestrating the complete flow: config → fetch → send."""
    try:
        logger.info("=" * 50)
        logger.info("Starting b2bflow WhatsApp Message Sender")
        logger.info("=" * 50)

        logger.info("Step 1: Loading configuration...")
        config = load_config()
        logger.info("✓ Configuration loaded successfully")

        logger.info("Step 2: Fetching contacts from Supabase...")
        contacts = fetch_contacts(config, limit=3)

        if not contacts:
            logger.error("✗ No contacts found. Aborting.")
            return 1

        logger.info(f"✓ Found {len(contacts)} contact(s)")

        logger.info("Step 3: Sending WhatsApp messages...")
        results = send_messages(config, contacts)

        logger.info("=" * 50)
        logger.info("Final Summary:")
        logger.info(f"  Total contacts: {results['total']}")
        logger.info(f"  Successfully sent: {results['sent']}")
        logger.info(f"  Failed: {results['failed']}")
        logger.info("=" * 50)

        if results["sent"] > 0:
            logger.info("✓ Process completed successfully!")
            return 0

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