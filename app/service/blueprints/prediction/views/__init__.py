import sanic


__all__ = ["prediction_blueprint"]

prediction_blueprint = sanic.Blueprint("predictions", version=1)


@prediction_blueprint.route("/predict", methods=["POST"])
async def predict_view(request: sanic.Request) -> sanic.HTTPResponse:
    text = request.json['text']
    return sanic.json({"sentiment": request.app.ctx.predictor.predict(text)})


@prediction_blueprint.route("/predict-sentence", methods=['POST'])
async def predict_sentence_view(request: sanic.Sanic) -> sanic.HTTPResponse:
    text = request.json['text']
    output = {}
    for sentence in request.app.ctx.splitter.split(text):
        output[sentence] = request.app.ctx.predictor.predict(sentence)
    return sanic.json(output)
