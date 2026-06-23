from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Credit Card Customer Churn Analytics Platform"
    environment: str = "development"
    postgres_user: str = "churn_user"
    postgres_password: str = ""
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_database: str = "churn_analytics"
    raw_data_path: Path = Path("../data/raw/BankChurners.csv")
    model_artifact_path: Path = Path("../data/artifacts/model.joblib")
    metrics_artifact_path: Path = Path("../data/artifacts/metrics.json")
    pr_curve_artifact_path: Path = Path("../data/artifacts/precision_recall_curve.json")
    shap_artifact_path: Path = Path("../data/artifacts/shap_summary.json")
    allowed_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[3]

    def resolve_path(self, path: Path) -> Path:
        if path.is_absolute():
            return path
        cwd_path = Path.cwd() / path
        if cwd_path.exists():
            return cwd_path
        return self.project_root / path


@lru_cache
def get_settings() -> Settings:
    return Settings()
