from pathlib import Path
import os


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

        self._env = self._load_env_file()
        self.database_url = self._get(
            "DATABASE_URL",
            "postgresql://postgres:password12@localhost:5432/mydatabase",
        )
        self.app_name = self._get("APP_NAME", "Navikenz Auth API")
        self.secret_key = self._get("SECRET_KEY", "change-this-secret-key")
        self.debug = self._get("DEBUG", "False").lower() == "true"
        self.cors_origins = [
            origin.strip()
            for origin in self._get("CORS_ORIGINS", "http://localhost:5173").split(",")
            if origin.strip()
        ]
        self._initialized = True

    def _load_env_file(self):
        env_path = Path(__file__).resolve().parents[1] / ".env"
        values = {}

        if not env_path.exists():
            return values

        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")

        return values

    def _get(self, key, default):
        return os.environ.get(key, self._env.get(key, default))


settings = Settings()
