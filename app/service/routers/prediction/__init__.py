from typing import List

from fastapi import APIRouter, Request

from .models import PredictInputModel, PredictResponseModel

__all__ = ["router"]

router = APIRouter()


@router.post("/predict", response_model=List[PredictResponseModel])
async def predict_on_full_text(body: PredictInputModel, request: Request) -> List[PredictResponseModel]:
    output = PredictResponseModel(
        start=0,
        stop=len(body.text),
        sentiment=request.app.state.predictor.predict(body.text),
    )
    return [output]


@router.post("/predict-sentence", response_model=List[PredictResponseModel])
async def predict_on_sentences(body: PredictInputModel, request: Request) -> List[PredictResponseModel]:
    input_text = body.text
    sentences = request.app.state.splitter.split(input_text)
    output: List[PredictResponseModel] = []
    last_stop = None
    for sentence in sentences:
        sentence_start = input_text.index(sentence, last_stop)
        sentence_stop = sentence_start + len(sentence)
        output.append(
            PredictResponseModel(
                start=sentence_start,
                stop=sentence_stop,
                sentiment=request.app.state.predictor.predict(sentence),
            )
        )
        last_stop = sentence_stop
    return output


@router.post("/predictions")
async def save_prediction():
    pass


@router.get("/predictions")
async def get_all_predictions():
    pass


@router.get("/predictions/{prediction_id}")
async def get_prediction_by_id(prediction_id: int):
    pass
