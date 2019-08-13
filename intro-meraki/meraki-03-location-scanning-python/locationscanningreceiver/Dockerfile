FROM python:3.6-alpine

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "locationscanningreceiver.py", "-v", "5d6d070c526bc5aad1bcf0228e3b1bc4ef5303d0", "-s", "5d6d070c526bc5aad1bcf0228e3b1bc4ef5303d0"]

