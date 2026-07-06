from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # Application settings
    APP_NAME: str = "My FastAPI Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database settings
    DATABASE_URL: str 
    REDIS_URL: str

    # Security settings
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ANTHROPIC_API_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()