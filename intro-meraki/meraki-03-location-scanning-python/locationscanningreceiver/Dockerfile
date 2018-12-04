FROM python:3.6-alpine

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "locationscanningreceiver.py", "-v", "simulator", "-s", "simulator"]
