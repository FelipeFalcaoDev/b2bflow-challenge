"""
Supabase client module for b2bflow-challenge.

Handles database communication for contact retrieval.
Single responsibility: fetch and validate contacts only.
"""

import logging
from typing import List

from supabase import create_client
from supabase.client import Client

from src.config import Config

logger = logging.getLogger(__name__)


class SupabaseContactFetcher:
    """
    Fetches and validates contacts from Supabase.

    Applies SRP: only handles database operations, not message formatting
    or WhatsApp communication.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize Supabase client.

        Args:
            config: Config instance with database credentials.

        Raises:
            ValueError: If connection fails.
        """
        try:
            self.client: Client = create_client(
                config.supabase_url, config.supabase_api_key
            )
            self.table_name: str = config.supabase_table_name
            logger.info(f"✓ Connected to Supabase table: {self.table_name}")
        except Exception as error:
            logger.error(f"✗ Failed to connect to Supabase: {error}")
            raise ValueError(f"Supabase connection error: {error}") from error

    def fetch_contacts(self, limit: int = 3) -> List[dict]:
        """
        Fetch contacts from database.

        Limit defaults to 3 to comply with Z-API free tier quotas.

        Args:
            limit: Max contacts to retrieve (default: 3).

        Returns:
            List of validated contact dictionaries with 'name' and 'phone'.

        Raises:
            ValueError: If query fails or no valid contacts found.
        """
        try:
            logger.info(f"Fetching up to {limit} contact(s) from Supabase...")

            response = (
                self.client.table(self.table_name)
                .select("*")
                .limit(limit)
                .execute()
            )

            if not response.data:
                logger.warning("No contacts found in database.")
                return []

            contacts = self._validate_contacts(response.data)
            logger.info(f"✓ Successfully fetched {len(contacts)} contact(s)")
            return contacts

        except Exception as error:
            logger.error(f"✗ Failed to fetch contacts: {error}")
            raise ValueError(f"Database query error: {error}") from error

    @staticmethod
    def _validate_contacts(contacts: List[dict]) -> List[dict]:
        """
        Validate contacts have required fields.

        Skips invalid contacts and logs warnings for debugging.

        Args:
            contacts: Raw contact list from database.

        Returns:
            List of validated contacts.

        Raises:
            ValueError: If no valid contacts found after validation.
        """
        validated: List[dict] = []

        for index, contact in enumerate(contacts):
            if not isinstance(contact, dict):
                logger.warning(f"Contact {index} is not a dictionary, skipping.")
                continue

            name = contact.get("name", "").strip()
            phone = contact.get("phone", "").strip()

            if not name or not phone:
                logger.warning(
                    f"Contact {index} missing name or phone, skipping: {contact}"
                )
                continue

            validated.append({"name": name, "phone": phone})

        if not validated:
            raise ValueError("No valid contacts found after validation.")

        return validated

def fetch_contacts(config: Config, limit: int = 3) -> List[dict]:
    """
    Factory function to fetch contacts from Supabase.

    Args:
        config: Config instance with database credentials.
        limit: Max contacts to fetch.

    Returns:
        List of validated contact dictionaries.

    Raises:
        ValueError: If connection or query fails.
    """
    fetcher = SupabaseContactFetcher(config)
    return fetcher.fetch_contacts(limit)