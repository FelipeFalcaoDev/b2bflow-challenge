"""
Configuration module for b2bflow-challenge.

Loads and validates environment variables from .env file.
All external credentials and URLs are centralized here.
"""

import logging
import os
from typing import Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class Config:
    """
    Loads and validates environment variables.

    Follows Single Responsibility Principle: only this class knows about
    environment variables. Other modules request what they need from here.
    """

    def __init__(self) -> None:
        """
        Load and validate all required environment variables.

        Raises:
            ValueError: If any required variable is missing or empty.
        """
        load_dotenv()

        # Supabase credentials
        self.supabase_url: str = self._get_required_env("SUPABASE_URL")
        self.supabase_api_key: str = self._get_required_env("SUPABASE_API_KEY")
        self.supabase_table_name: str = self._get_required_env(
            "SUPABASE_TABLE_NAME", default="contacts"
        )

        # Z-API endpoint (includes instance ID and token)
        self.zapi_url: str = self._get_required_env("ZAPI_URL")

        logger.info("✓ Configuration loaded and validated")

    @staticmethod
    def _get_required_env(
        variable_name: str, default: Optional[str] = None
    ) -> str:
        """
        Retrieve and validate an environment variable.

        Args:
            variable_name: Name of the environment variable.
            default: Optional default value if variable not set.

        Returns:
            The environment variable value.

        Raises:
            ValueError: If variable is missing and no default provided.
        """
        value = os.getenv(variable_name, default)

        if value is None:
            raise ValueError(
                f"Environment variable '{variable_name}' is required but not set. "
                f"Check your .env file."
            )

        if not value.strip():
            raise ValueError(
                f"Environment variable '{variable_name}' is empty. "
                f"Provide a valid value in your .env file."
            )

        return value

def load_config() -> Config:
    """
    Factory function to load configuration.

    Returns:
        Config instance with all required variables validated.

    Raises:
        ValueError: If any configuration is invalid.
    """
    try:
        return Config()
    except ValueError as error:
        logger.error(f"Configuration error: {error}")
        raise ValueError(f"Configuration error: {error}") from error