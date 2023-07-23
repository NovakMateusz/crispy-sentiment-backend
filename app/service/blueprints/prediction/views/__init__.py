import asyncio
import typing

import sanic
from tortoise.transactions import in_transaction

from app.core.db.models import Predictions, PredictionAnnotations, Users
from app.service.utils.decorators import authorized


__all__ = ["prediction_blueprint"]

prediction_blueprint = sanic.Blueprint("predictions", version=1)


@prediction_blueprint.route("/predict", methods=["POST"])
async def predict_view(request: sanic.Request) -> sanic.HTTPResponse:
    text = request.json["text"]
    return sanic.json(
        [
            {
                "start": 0,
                "stop": len(text),
                "sentiment": request.app.ctx.predictor.predict(text),
            }
        ]
    )


@prediction_blueprint.route("/predict-sentence", methods=["POST"])
async def predict_sentence_view(request: sanic.Request) -> sanic.HTTPResponse:
    input_text = request.json["text"]
    sentences = request.app.ctx.splitter.split(input_text)
    output: typing.List[typing.Dict[str, typing.Any]] = []
    last_stop = None
    for sentence in sentences:
        if sentence != "":
            sentence_start = input_text.index(sentence, last_stop)
            sentence_stop = sentence_start + len(sentence)
            output.append(
                {
                    "start": sentence_start,
                    "stop": sentence_stop,
                    "sentiment": request.app.ctx.predictor.predict(sentence),
                }
            )
            last_stop = sentence_stop
    return sanic.json(output)


@prediction_blueprint.route("/save-prediction", methods=["POST"])
@authorized()
async def save_prediction_view(request: sanic.Request, user_id: int) -> sanic.HTTPResponse:
    input_model = request.json
    text = input_model["raw-text"]
    annotations = input_model["annotations"]

    async with in_transaction() as async_connection:
        user = await Users.filter(id=user_id).first()
        new_prediction = Predictions(user=user, raw_text=text)
        await new_prediction.save(using_db=async_connection)
        await asyncio.gather(
            *[
                PredictionAnnotations(
                    prediction=new_prediction,
                    sentiment=annotation["sentiment"],
                    start=annotation["start"],
                    stop=annotation["stop"],
                ).save(using_db=async_connection)
                for annotation in annotations
            ]
        )

    return sanic.json({})


@prediction_blueprint.route("/get-predictions")
@authorized()
async def get_user_predictions_view(_: sanic.Request, user_id: int) -> sanic.HTTPResponse:
    predictions = await Predictions.filter(user_id=user_id).all()
    response: typing.List[typing.Dict[str, typing.Any]] = []
    for prediction in predictions:
        response.append({"id": prediction.id, "text": prediction.raw_text})
    return sanic.json(response)


@prediction_blueprint.route("/get-prediction/<prediction_id:int>")
@authorized()
async def get_user_prediction_view(
    _: sanic.Request, user_id: int, prediction_id: int
) -> sanic.HTTPResponse:
    prediction = (
        await Predictions.filter(id=prediction_id, user_id=user_id)
        .prefetch_related("prediction_annotations")
        .first()
    )

    if not prediction:
        return sanic.json({})

    response: typing.Dict[str, typing.Any] = {
        "text": prediction.raw_text,
        "annotations": [],
    }

    for annotation in prediction.prediction_annotations:
        response["annotations"].append(
            {"sentiment": annotation.sentiment, "start": annotation.start, "stop": annotation.stop}
        )

    return sanic.json(response)
