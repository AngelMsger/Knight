FROM python

MAINTAINER "i@AngelMsger"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

VOLUME ["/app/cache"]

CMD ["python", "robot.py"]
