```bash
pip3 install --upgrade pip
pip3 install pip-tools
pip-compile --generate-hashes --no-emit-index-url requirements/core.in

pip install --require-hashes -r requirements/core.txt

uvicorn --host "0.0.0.0" --port "8000" --loop "uvloop" --http "httptools" --no-access-log  --factory "app.service:create_app"
```


```bash
pip install typer
pip install boto3
```
