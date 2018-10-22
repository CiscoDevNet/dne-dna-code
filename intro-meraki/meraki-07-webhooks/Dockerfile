FROM python:3.6-alpine

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5005

CMD ["python", "webhookreceiver.py", "-s", "webbie"]
