FROM python:3.6-alpine

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5004

CMD python cmxnotificationreceiver.py -u learning -p learning -l cmxlocationsandbox.cisco.com -i mjd
