FROM python:3.7

RUN mkdir -p /usr/src/app/alice

WORKDIR /usr/src/app/alice/

COPY . /usr/src/app/alice/

RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5057
CMD ["python", "main.py"]
