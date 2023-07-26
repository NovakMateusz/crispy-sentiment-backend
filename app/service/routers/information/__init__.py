from fastapi import APIRouter, Request

from .models import InformationResponseModel, ModelMetrics

__all__ = ["router"]

router = APIRouter()


@router.get("/information")
async def get_model_info(request: Request) -> InformationResponseModel:
    model_info = request.app.state.predictor.get_info()

    return InformationResponseModel(
        hash=model_info['hash'],
        name=model_info['name'],
        metrics=ModelMetrics(
            precision=float(model_info['metrics']['precision']),
            recall=float(model_info['metrics']['recal']),
            f1=float(model_info['metrics']['f1']),
        ),
    )
