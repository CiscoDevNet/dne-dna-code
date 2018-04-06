FROM python:3.6-alpine

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5002

CMD ["python", "locationscanningsimulator.py"]
