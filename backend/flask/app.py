# -*- coding: utf-8 -*-
import json
from flask import Flask, Response
from kubernetes import client, config

import dbutil

app = Flask(__name__)
PORT = "3307"


@app.route("/model", methods=["GET"])
def get_model_info():
  # TODO try ~ exception ~ finally 로 변경
  sqlOutput = dbutil.select_model_info()

  if len(sqlOutput) is 0:
    return {'StatusCode': '500', 'Message': 'There isn\'t any  model info'}
  else:
    msg = json.dumps(sqlOutput, ensure_ascii=False)  # 한글 인코딩

    response = Response(msg, status=200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"  # text/html 로?
    return response


@app.route("/test", methods=["POST"])
def create_ae_job():
  # pod 에서 client 사용하려면 sa 사용해서 config load 해야 함
  config.load_incluster_config()
  batchApi = client.BatchV1Api()

  job = client.V1Job()

  # TODO job spec 만드는 것 k8s_util.py 분리해서 함수화
  label = dict()
  label['mlmodel'] = 'ae'
  job.metadata = client.V1ObjectMeta(name="ae",  # 이름 겹치지 않게 generator 사용
                                     labels=label)

  in_hostpath = client.V1HostPathVolumeSource(path='/hosthome/kjy/input/',
                                              type='Directory')
  in_volume = client.V1Volume(name='in-storage', host_path=in_hostpath)

  out_hostpath = client.V1HostPathVolumeSource(path='/mnt/sda1/data/',
                                               type='Directory')
  out_volume = client.V1Volume(name='out-storage', host_path=out_hostpath)

  container_port = client.V1ContainerPort(container_port=3307)

  in_volume_mount = client.V1VolumeMount(mount_path='/input',
                                         name='in-storage')
  out_volume_mount = client.V1VolumeMount(mount_path='/output',
                                          name='out-storage')
  container = client.V1Container(name='ae',
                                 image='192.1.4.75:5000/model-ae:v0.1.5',
                                 image_pull_policy='Always',
                                 ports=[container_port],
                                 volume_mounts=[in_volume_mount,
                                                out_volume_mount]
                                 )

  podSpec = client.V1PodSpec(service_account_name='kjy',
                             restart_policy='OnFailure',
                             containers=[container],
                             volumes=[in_volume, out_volume])
  template = client.V1PodTemplateSpec(spec=podSpec)

  spec = client.V1JobSpec(template=template, backoff_limit=3)
  job.spec = spec

  # TODO 이거 주위로 kubernetes.client.rest.ApiException 감싸기
  batchApi.create_namespaced_job(namespace='default', body=job)  # sync call
  print('Job created')
  print(str(job))

  # TODO Job completed wait
  return Response("Job Created", status=200)

  # TODO 공유 후 삭제
  # # busybox pod 생성
  # pod = client.V1Pod()
  # pod.metadata = client.V1ObjectMeta(name="busybox-python")
  #
  # container = client.V1Container(name="busybox", image="busybox",
  #                                image_pull_policy="IfNotPresent")
  # container.args = ["sleep", "3600"]
  #
  # spec = client.V1PodSpec(containers=[container], restart_policy="Always")
  # pod.spec = spec
  #
  # v1.create_namespaced_pod(namespace="default", body=pod)  # sync call
  # print("Pod deployed.")


@app.route("/", methods=["GET"])
def hello():
  return "Hello Flask!"


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=PORT, debug=True)
