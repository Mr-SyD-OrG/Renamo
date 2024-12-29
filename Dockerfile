FROM python:3.10
WORKDIR /app
COPY . /app/
RUN apt-get install -y ffmpeg && \
    pip install -r requirements.txt
    
CMD ["python", "bot.py"]
