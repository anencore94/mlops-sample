FROM python:3.6

ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

EXPOSE 3307

# 패키지 버전 정리 후 requirements.txt 로 install
RUN pip install flask flask-mysql kubernetes

COPY flask ./flask

CMD ["python", "./flask/app.py"]