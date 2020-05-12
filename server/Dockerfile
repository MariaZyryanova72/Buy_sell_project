FROM python:3.7

RUN mkdir -p /usr/src/app/server/

WORKDIR /usr/src/app/server/

COPY . /usr/src/app/server/

RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5055
CMD ["python", "main.py"]