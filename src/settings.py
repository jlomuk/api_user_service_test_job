from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    POSTGRES_URL: PostgresDsn
    POSTGRES_TEST_URL: PostgresDsn

    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600  # 5 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # 3 days
    ALGORITHM: str = "HS256"

    SALT_FOR_PASSWORD: str = 'Fof'

    class Config:
        env_file = '.env'


settings = Settings()  
