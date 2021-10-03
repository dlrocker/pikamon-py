FROM python:3.9.7-alpine

WORKDIR /bot
ENV PYTHONPATH "${PYTHONPATH}:/bot/pikamon"
COPY requirements.txt .
# First run command is to build gcc for Python dependencies
RUN apk add build-base && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    # Create the bot SQLite data, configuration, and source code directories under the working directory
    mkdir data && \
    mkdir configuration && \
    mkdir pikamon
COPY configuration /bot/configuration
COPY pikamon /bot/pikamon

CMD ["python3", "/bot/pikamon/bot.py"]
