import pathlib
import pickle
import typing

import aiofile
from sklearn.base import BaseEstimator


__all__ = ["Predictor"]


class Predictor:
    def __init__(self, model_path: pathlib.Path) -> None:
        self._model_path: pathlib.Path = model_path
        self._model_name: str
        self._model_hash: str
        self._model_metrics: typing.Dict
        self._labels: typing.Dict
        self._vectorizer: BaseEstimator
        self._model: BaseEstimator

    async def async_load(self) -> None:
        async with aiofile.async_open(self._model_path, "rb") as afp:
            pickle_data = pickle.loads(await afp.read())
            self._parse_pickle_data(pickle_data)

    def load(self) -> None:
        with open(self._model_path, "rb") as fp:
            pickle_data = pickle.loads(fp.read())
            self._parse_pickle_data(pickle_data)

    def _parse_pickle_data(self, pickle_data: typing.Dict) -> None:
        self._model_hash = pickle_data["model_hash"]
        self._model_name = pickle_data["model_name"]
        self._model_metrics = pickle_data["metrics"]
        self._model = pickle_data["model"]
        self._vectorizer = pickle_data["vectorizer"]
        self._labels = pickle_data["labels"]

    def get_info(self) -> typing.Dict:
        return {"name": self._model_name, "hash": self._model_hash, "metrics": self._model_metrics}

    def predict(self, text: str) -> str:
        vector = self._vectorizer.transform([text])
        return self._labels[self._model.predict(vector)[0]]
