import logging
from typing import List
from supabase import create_client
from supabase.client import Client
from src.config import Config

logger = logging.getLogger(__name__)

class SupabaseContactFetcher:
    def __init__(self, config: Config) -> None:
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
        try:
            logger.info(f"Fetching up to {limit} contacts from Supabase...")
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
        validated: List[dict] = []
        for index, contact in enumerate(contacts):
            if not isinstance(contact, dict):
                logger.warning(f"Contact at index {index} is not a dictionary, skipping.")
                continue

            name = contact.get("name", "").strip()
            phone = contact.get("phone", "").strip()

            if not name or not phone:
                logger.warning(
                    f"Contact at index {index} missing name or phone, skipping: {contact}"
                )
                continue

            validated.append({"name": name, "phone": phone})

        if not validated:
            raise ValueError("No valid contacts found after validation.")

        return validated

def fetch_contacts(config: Config, limit: int = 3) -> List[dict]:
    fetcher = SupabaseContactFetcher(config)
    return fetcher.fetch_contacts(limit)