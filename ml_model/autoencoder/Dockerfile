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
COPY datasets ./datasets
# TODO data 는 pvc 에 저장하고 pod 에선 mount 해서 사용하도록 변경

# library 들이 너무 커서 build 시간 너무 오래 걸림..
RUN pip install -r requirements.txt

# TODO ml_model 의 output 을 정리해서 RWM pvc 에 저장
RUN mkdir -p ./ex_1
RUN echo "python ./train.py > ./ex_1/train_stat && sleep 3600" >> ./start.sh && \
chmod 777 ./start.sh

CMD ["sh","-c","./start.sh"]