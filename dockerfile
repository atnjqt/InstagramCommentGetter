FROM python:3.7-slim

COPY GetComments.py /app/GetComments.py

COPY configs /app/configs

WORKDIR /app

RUN pip install -r /app/configs/requirements.txt

# YOU MUST ENTER INSTAGRAM URL AS ARGUMENT...
# Is there a way to pass this into the file for dockerfiles?

CMD ["python3", "GetComments.py", "https://www.instagram.com/p/B714x80nmXs"]
