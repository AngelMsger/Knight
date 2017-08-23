FROM python

MAINTAINER AngelMsger

COPY . /app

WORKDIR /app

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

VOLUME ["/app/cache"]

CMD ["python", "robot.py"]
