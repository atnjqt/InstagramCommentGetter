FROM python:3.7-slim

COPY GetComments.py /app/GetComments.py

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

# Unbuffered to display stdout for print statements
ENV PYTHONUNBUFFERED=1 

# YOU MUST ENTER INSTAGRAM URL AS ARGUMENT...
# Using test URL... but the previous process I had jhub notebook
# which looped through wwe_df.posturl.unique() editing dockerfile template
# guessing there is a better way to do this
# either w env var or volume mount
CMD ["python3", "GetComments.py", "https://www.instagram.com/p/B8H0UX4J-8z/"]
