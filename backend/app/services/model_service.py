import json

import joblib

from app.core.config import get_settings
from app.schemas.customer import PredictionRequest, PredictionResponse
from ml.features import build_prediction_frame


def risk_band(probability: float) -> str:
    if probability >= 0.7:
        return "High"
    if probability >= 0.4:
        return "Medium"
    return "Low"


def recommended_action(probability: float) -> str:
    if probability >= 0.7:
        return "Priority retention call with fee review or tailored rewards offer."
    if probability >= 0.4:
        return "Monitor engagement and send proactive product education campaign."
    return "Maintain standard lifecycle communication."


class ChurnModelService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._artifact: dict | None = None
        self._shap_summary: list[dict] | None = None

    def _load_artifact(self) -> dict:
        if self._artifact is None:
            artifact_path = self.settings.resolve_path(self.settings.model_artifact_path)
            if not artifact_path.exists():
                raise FileNotFoundError(
                    f"Model artifact not found at {artifact_path}. Run backend/scripts/train_model.py first."
                )
            self._artifact = joblib.load(artifact_path)
        return self._artifact

    def _load_shap_summary(self) -> list[dict]:
        if self._shap_summary is None:
            shap_path = self.settings.resolve_path(self.settings.shap_artifact_path)
            if shap_path.exists():
                self._shap_summary = json.loads(shap_path.read_text(encoding="utf-8"))
            else:
                self._shap_summary = []
        return self._shap_summary

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        artifact = self._load_artifact()
        frame = build_prediction_frame(request.model_dump())
        probability = float(artifact["pipeline"].predict_proba(frame)[0, 1])
        drivers = self._load_shap_summary()[:5]

        return PredictionResponse(
            churn_probability=probability,
            risk_band=risk_band(probability),
            recommended_action=recommended_action(probability),
            top_drivers=drivers,
        )


model_service = ChurnModelService()
