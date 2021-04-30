# -*- coding: utf-8 -*-
"""
API server
"""
import json

from flask import Flask, Response, request
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from werkzeug.exceptions import BadRequestKeyError

import const
import db_util
import k8s_util

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_model_info():
  """
  MODEL_INFO table 의 모든 row 를 조회합니다.

  :return: 조회결과와 HTTP_STATUS 를 담은 Response
  :rtype: Response
"""
  # TODO try ~ exception ~ finally 로 변경
  sql_output = db_util.select_model_info()

  if len(sql_output) == 0:
    return {'StatusCode': '400', 'Message': 'There isn\'t any  model info'}

  msg = json.dumps(sql_output, ensure_ascii=False)  # 한글 인코딩
  response = Response(msg, status=200)
  response.headers["Access-Control-Allow-Origin"] = "*"
  response.headers["Content-Type"] = "application/json"  # text/html 로?

  return response


@app.route("/test", methods=["POST"])
def create_ae_job():
  """
autoencoer 학습을 진행하는 k8s job 을 하나 생성합니다.

:param: learning_rate, epoch, experiment_id
:return: 생성 여부와 HTTP_STATUS 를 담은 Response
:rtype: Response
"""

  # STEP 1) request body 에서 필요한 정보 파싱
  # TODO UI 에서 보낼 때, json 인지 form 인지에 따라 추후 변경 필요할 수도 있음
  try:
    req_lr = request.form['learning_rate']
    req_epoch = request.form['epoch']
    req_ex_id = request.form['experiment_id']
  except BadRequestKeyError as e:
    print(e)
    return Response("Wrong Input. Please check your request body", status=400)

  # STEP 2) DB 에 experiment 정보 저장
  # DB 에서 data file path 조회

  # STEP 3) k8s job 생성 요청
  # pod 에서 client 사용하려면 sa 사용해서 config load 해야 함
  config.load_incluster_config()
  # client 만들기
  batch_api_client = client.BatchV1Api()
  try:
    batch_api_client.create_namespaced_job(namespace='default',
                                           body=
                                           k8s_util.make_job_spec(
                                             lr=req_lr, epoch=req_epoch,
                                             ex_id=req_ex_id))  # sync call
    # 여기서 timeout 걸릴 경우 고려 필요
  except ApiException as e:
    print(e)
    return Response("Job Creation Failed", status=400)

  # STEP 4) k8s job 이 Completed 될 때까지 wait

  # STEP 5) DB 에 output_file_path 저장

  # STEP 6) 성공/실패 여부 반환
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
  return "Welcome to Makinarocks!"


@app.route("/hello", methods=["GET"])
def hello_adp():
  return "Hello ADP"


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=const.FLASK_PORT, debug=True)
