from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password12@localhost:5432/mydatabase"
    APP_NAME: str = "Navikenz Auth API"
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174,http://localhost:5175,http://127.0.0.1:5175,http://localhost:5176,http://127.0.0.1:5176,http://localhost:5177,http://127.0.0.1:5177"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


class SettingsSingleton:
    _instance: Settings | None = None

    @classmethod
    def get_settings(cls) -> Settings:
        if cls._instance is None:
            cls._instance = Settings()
        return cls._instance


settings = SettingsSingleton.get_settings()
