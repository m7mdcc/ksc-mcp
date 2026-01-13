from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    KSC_HOST: str
    KSC_USERNAME: str
    KSC_PASSWORD: str
    KSC_VERIFY_SSL: bool = True

    # Optional: Port if not included in HOST (KlAkOAPI handles this, but good to have)
    KSC_PORT: int = 13299
    
    # Optional: Path to SSL certificate for verification
    KSC_CERT_PATH: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
