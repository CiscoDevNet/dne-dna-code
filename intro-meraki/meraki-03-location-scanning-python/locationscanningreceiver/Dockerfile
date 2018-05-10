FROM python:3.6-alpine

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5001

CMD python locationscanningreceiver.py -v 9954e8cc03bbd5063df927a1e76925e09a40c032 -s scanninglab
