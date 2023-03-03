FROM python:3.11.2-bullseye
LABEL maintainer="Mateusz Nowak <novak.mateusz94@gmail.com>"

RUN apt update -y && apt upgrade -y

ENV VIRTUAL_ENVIRONEMT=/crispy_sentiment/venv
WORKDIR /crispy_sentiment
RUN python3 -m venv $VIRTUAL_ENVIRONEMT
ENV PATH="$VIRTUAL_ENVIRONEMT/bin:$PATH"

RUN mkdir -p app/artifacts
COPY app/core app/core
COPY app/service app/service
COPY requirements/core.txt core.txt

RUN ["python", "-m", "pip", "install", "-r", "core.txt"]

RUN groupadd -g 333 crispyGroup && useradd -r -u 333 -g crispyGroup crispyUser && chown -R crispyUser /crispy_sentiment
USER crispyUser

EXPOSE 8000
CMD ["python3", "-m", "sanic", "--factory", "app.service:create_app", "--host", "0.0.0.0", "--port", "8000", "--loop", "uvloop", "--no-access-log"]
