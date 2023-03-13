import sanic


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
async def predict_sentence_view(request: sanic.Sanic) -> sanic.HTTPResponse:
    input_text = request.json["text"]
    sentences = request.app.ctx.splitter.split(input_text)
    output = []
    last_stop = None
    for sentence in sentences:
        if sentence != "":
            sentence_start = input_text.index(sentence, last_stop)
            sentence_stop =  sentence_start + len(sentence)
            output.append(
                {
                    "start": sentence_start,
                    "stop": sentence_stop,
                    "sentiment": request.app.ctx.predictor.predict(sentence),
                }
            )
            last_stop = sentence_stop
    return sanic.json(output)
