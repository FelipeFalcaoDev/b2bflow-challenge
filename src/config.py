import os
from typing import Optional
from dotenv import load_dotenv

class Config:
    def __init__(self) -> None:
        load_dotenv()
        self.supabase_url: str = self._get_required_env("SUPABASE_URL")
        self.supabase_api_key: str = self._get_required_env("SUPABASE_API_KEY")
        self.supabase_table_name: str = self._get_required_env(
            "SUPABASE_TABLE_NAME", default="contacts"
        )
        self.zapi_url: str = self._get_required_env("ZAPI_URL")
        self.zapi_token: str = self._get_required_env("ZAPI_TOKEN")

    @staticmethod
    def _get_required_env(variable_name: str, default: Optional[str] = None) -> str:
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
    try:
        return Config()
    except ValueError as error:
        raise ValueError(f"Configuration error: {error}") from error