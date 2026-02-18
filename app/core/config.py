from pydantic import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "Enterprise Voice Obfuscator"

    MAX_FILE_SIZE_MB: int = 20

    SAMPLE_RATE: int = 16000

    SECRET_KEY: str = "super-secret-key"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
