import asyncio
from typing import Any, Dict, List
from uuid import UUID

from sanic import Blueprint, Request, HTTPResponse, json
from tortoise.transactions import in_transaction

from app.core.database.models import Predictions, PredictionAnnotations, Users
from app.service.blueprints.v1.predict.models import (
    PredictInputModel,
    PredictResponseModel,
    SavePredictionInputModel,
    UserPredictionResponseModel,
)
from app.service.utils.decorators import authorized, validate

__all__ = ["blueprint"]


blueprint = Blueprint("predict")


@blueprint.route("/predict", methods=["POST", "OPTIONS"])
@validate(model=PredictInputModel)
async def predict_view(request: Request, input_model: PredictInputModel) -> HTTPResponse:
    output_model = PredictResponseModel(
        start=0, stop=len(input_model.text), sentiment=request.app.ctx.predictor.predict(input_model.text)
    )
    return json([output_model.model_dump()])


@blueprint.route("/predict-sentence", methods=["POST", "OPTIONS"])
@validate(model=PredictInputModel)
async def predict_on_sentences_view(request: Request, input_model: PredictInputModel) -> HTTPResponse:
    sentences = request.app.ctx.splitter.split(input_model.text)
    output: List[Dict[str, Any]] = []
    last_stop = None
    for sentence in sentences:
        sentence_start = input_model.text.index(sentence, last_stop)
        sentence_stop = sentence_start + len(sentence)
        output.append(
            PredictResponseModel(
                start=sentence_start,
                stop=sentence_stop,
                sentiment=request.app.ctx.predictor.predict(sentence),
            ).model_dump()
        )
        last_stop = sentence_stop
    return json(output)


@blueprint.route("/predictions", methods=["POST", "OPTIONS"])
@authorized()
@validate(model=SavePredictionInputModel)
async def save_prediction_view(_: Request, input_model: SavePredictionInputModel, user: Users) -> HTTPResponse:
    async with in_transaction() as async_connection:
        new_prediction = Predictions(user_id=user.id, raw_text=input_model.raw_text)
        await new_prediction.save(using_db=async_connection)
        await asyncio.gather(
            *[
                PredictionAnnotations(
                    prediction=new_prediction,
                    sentiment=annotation.sentiment,
                    start=annotation.start,
                    stop=annotation.stop,
                ).save(using_db=async_connection)
                for annotation in input_model.annotations
            ]
        )

    return json({"message": "Prediction saved"})


@blueprint.route("/predictions")
@authorized()
async def get_user_predictions_view(_: Request, user: Users) -> HTTPResponse:
    predictions = await Predictions.filter(user_id=user.id).all()
    response: List[Dict[str, Any]] = []
    for prediction in predictions:
        response.append({"id": str(prediction.id), "text": prediction.raw_text})
    return json(response)


@blueprint.route("/predictions/<prediction_id:uuid>", methods=["GET", "OPTIONS", "DELETE"])
@authorized()
async def get_user_prediction_by_id_view(request: Request, user: Users, prediction_id: UUID) -> HTTPResponse:
    if request.method == "DELETE":
        async with in_transaction() as async_connection:
            prediction = (
                await Predictions.filter(id=prediction_id, user_id=user.id)
                .prefetch_related("prediction_annotations")
                .first()
            )
            if not prediction:
                return json({})

            await prediction.delete(using_db=async_connection)

        return json({"message": f"Prediction {prediction_id} has been deleted"})

    prediction = (
        await Predictions.filter(id=prediction_id, user_id=user.id).prefetch_related("prediction_annotations").first()
    )
    if not prediction:
        return json({})

    response = UserPredictionResponseModel(
        id=prediction_id,
        text=prediction.raw_text,
        annotations=[
            PredictResponseModel(start=annotation.start, stop=annotation.stop, sentiment=annotation.sentiment)
            for annotation in prediction.prediction_annotations
        ],
    )

    return json(response.model_dump())
