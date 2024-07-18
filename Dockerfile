FROM python:3.12.4-alpine3.20

RUN apk add --no-cache bash coreutils

COPY . .


RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements-dev.txt

# TODO: Add entry path
# CMD ["python", "samples/test.py"]