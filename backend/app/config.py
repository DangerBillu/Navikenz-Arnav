import os
from pathlib import Path


class Settings:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._load_env_file()
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
        self.app_name = os.getenv("APP_NAME", "Navikenz Auth API")
        self.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")
        self._initialized = True

    def _load_env_file(self):
        env_path = Path(__file__).resolve().parents[2] / ".env"
        if not env_path.exists():
            return

        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


settings = Settings()
