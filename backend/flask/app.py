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
def run_ad_pod():
  # pod 에서 client 사용하려면 sa 사용해서 config load 해야 함
  config.load_incluster_config()
  v1 = client.CoreV1Api()

  # busybox pod 생성
  pod = client.V1Pod()
  pod.metadata = client.V1ObjectMeta(name="busybox-python")

  container = client.V1Container(name="busybox", image="busybox",
                                 image_pull_policy="IfNotPresent")
  container.args = ["sleep", "3600"]

  spec = client.V1PodSpec(containers=[container], restart_policy="Always")
  pod.spec = spec

  v1.create_namespaced_pod(namespace="default", body=pod)
  print("Pod deployed.")

  return Response("Pod deployed", status=200)


@app.route("/", methods=["GET"])
def hello():
  return "Hello Flask!"


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=PORT, debug=True)
