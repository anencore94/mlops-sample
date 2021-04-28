FROM python:3.6

ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV DB_PORT 31111
ENV DB_USER testuser
ENV DB_PASSWORD testpassword
ENV DB_DATABASE testdb
#ENV AE_MODEL_IMAGE_URL localhost:5000/model-ae:v0.0.1

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

EXPOSE 3307

# 패키지 버전 정리 후 requirements.txt 로 install
RUN pip install flask flask-mysql kubernetes

COPY flask ./flask

CMD ["python", "./flask/app.py"]
