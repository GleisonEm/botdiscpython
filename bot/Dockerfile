FROM python:3.12

RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc g++ libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV TOKEN_DISCORD=${TOKEN_DISCORD}

CMD [ "python", "./main2.py" ]
