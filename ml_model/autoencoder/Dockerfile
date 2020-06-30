FROM python:3.6
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

EXPOSE 3307

COPY data.py .
COPY model.py .
COPY train.py .
COPY requirements.txt ./requirements.txt

# library 들이 너무 커서 build 시간 너무 오래 걸림..
RUN pip install -r requirements.txt

# TODO /output 디렉토리는 RWM pvc 로
RUN echo "mkdir -p /output/ex_1/ && python ./train.py > /output/ex_1/train_stat && sleep 10" >> ./start.sh && \
chmod 777 ./start.sh

CMD ["sh","-c","./start.sh"]