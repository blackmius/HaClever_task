FROM alpine:3.11 as base

RUN apk update && apk add --no-cache build-base python3-dev
RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN python3 -m pip install --user -r ./requirements.txt

FROM alpine:3.11

RUN apk update && apk add --no-cache python3

COPY --from=base /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /usr/src/app/

COPY src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]