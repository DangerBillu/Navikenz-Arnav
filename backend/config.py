from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password12@localhost:5432/mydatabase"
    APP_NAME: str = "Navikenz Auth API"
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174,http://localhost:5175,http://127.0.0.1:5175,http://localhost:5176,http://127.0.0.1:5176,http://localhost:5177,http://127.0.0.1:5177"
    AUTH0_DOMAIN: str = ""
    AUTH0_AUDIENCE: str = ""
    AUTH0_CLIENT_ID: str = ""
    VITE_AUTH0_CLIENT_ID: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    @property
    def auth0_audiences(self) -> list[str]:
        return [
            audience
            for audience in {
                self.AUTH0_AUDIENCE.strip(),
                self.AUTH0_CLIENT_ID.strip(),
                self.VITE_AUTH0_CLIENT_ID.strip(),
            }
            if audience
        ]


class SettingsSingleton:
    _instance: Settings | None = None

    @classmethod
    def get_settings(cls) -> Settings:
        if cls._instance is None:
            cls._instance = Settings()
        return cls._instance


settings = SettingsSingleton.get_settings()
