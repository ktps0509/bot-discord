FROM python:3.11
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot/
RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3-venv && \
    apt-get install -y ffmpeg && apt-get install libopus0
CMD python main.py