FROM python:3.6
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

EXPOSE 3307

# library 들이 너무 커서 build 시간 너무 오래 걸림..
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY data_preprocess.py .
COPY model.py .
COPY train.py .
COPY main.py .

# TODO /output 디렉토리는 RWM pvc 로
# mkdir 을 docker volume 하위 경로에 할 때에는 먼저 하면 안 되고, CMD 에서 해야 적용됨
CMD ["sh", "-c","mkdir -p $OUTPUT_MOUNT_POINT/$EXPERIMENT_ID && python ./main.py --learning_rate=$LEARNING_RATE --epoch=$EPOCH > $OUTPUT_MOUNT_POINT/$EXPERIMENT_ID/train_stat"]