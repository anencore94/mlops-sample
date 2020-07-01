# Backend Server
- flask 를 docker image 로 만들어 pod 으로 생성

## 요구 사항
- flask pod 내부에서 mysql DB pod 과 통신하여 다양한 sql query 수행
  - DB_IP 등 필요한 접속 정보를 flask 내부에서 os.getenv('key') 사용하도록 사전 구현해놓고, pod.yaml 의 env 로 주입
- flask pod 내부에서 k8s-api-server 와 통신하여 pod 생성, 조회 등의 다양한 k8s api 수행
  - serviceAccount, clusterRoleBinding 을 미리 생성하여 내부에서 load 하도록 구현해놓고, pod.yaml 에 sa name 명시
- flask pod 내부에서 host 의 특정 폴더를 input, output 폴더로 공유해서 사용
  - hostpath pvc 를 미리 생성하여 내부에서 사용하도록 구현해놓고, pod.yaml 에 pvc name 명시
  - 각각의 ml_model pod 도 동일한 hostpath pvc 공유해서 내부에서 사용하도록 RWM pvc 로 생성

## 구성 요소
- {setup/0, 1, 2, 3.yaml}
  - flask pod 이 사용할 pv, pvc, sa, crb 를 미리 생성
- 4_pod.yaml
- 5_svc.yaml
  - flask pod 의 IP 는 유동적인 값이므로, node 의 ip, port 를 사용하여 flask client 가 쉽게 접근할 수 있도록 일종의 port-forwarding 역할 수행

## 생성 방법
- docker registry 설정
- docker image push
  - `backend/build.sh` 의 `REPOSITORY_URL=localhost:5000` 를 custom docker registry 의 URL 로 수정 후 `./backend/build.sh` 실행
  - 정상 push 되었는지, 그리고 k8s cluster 안에서 접근 가능한지 확인
    - k8s cluster 내부 node 에서 다음 커맨드를 수행하여 방금 push 한 tag 의 image 가 존재하는지 확인
    - `curl -X GET http://localhost:5000/v2/hello-flask/tags/list`
- input, output 폴더로 사용할 host 의 hostname 과 경로를 수정
  - `yaml/setup/0_pv_input.yaml`, `yaml/setup/0_pv_output.yaml` 의 해당 부분 수정
- setup
  - `kubectl apply -f yaml/setup/0_pv_input.yaml`
  - `kubectl apply -f yaml/setup/0_pv_output.yaml`
  - `kubectl apply -f yaml/setup/1_pvc_input.yaml`
  - `kubectl apply -f yaml/setup/1_pvc_output.yaml`
  - `kubectl apply -f yaml/setup/2_sa.yaml`
  - `kubectl apply -f yaml/setup/3_crb.yaml`
- flask pod 생성
  - `kubectl apply -f yaml/4_pod.yaml`
    - flask_image_url, DB_IP, AE_MODEL_IMAGE_URL 를 수정한 후 apply 실행
  - `kubectl apply -f yaml/5_svc.yaml`

## API 확인 방법
- `GET {$Flask pod 이 떠있는 node 의 IP}:31112`
  - "Hello Flask!" 가 출력되는지 확인
- `GET {$Flask pod 이 떠있는 node 의 IP}:31112/model`
  - (DB pod 이 미리 생성되어 있어야 함)
  - json 형식의 experiment 정보가 출력되는지 확인
  - 혹시 `RuntimeError: cryptography is required for sha256_password or caching_sha2_password // Werkzeug Debugger` 에러 뜰 경우 `mysql -h 192.168.99.100 --port=31111 -u testuser -ptestpassword -D testdb` 를 수동으로 최초 한 번 접속해주면 해결될 수도 있음
- `POST {$Flask pod 이 떠있는 node 의 IP}:31112/test`
  - (autoencoder model 이미지가 미리 해당 repository 에 push 되어있어야 함)
  - request body 는 form-data 로 'learning_rate : {원하는 float 값}', 'epoch : {원하는 int 값}', 'experiment_id : {원하는 str 값}' 을 담아 http request
  - response
    - Job Created 나오면 `kubectl get job` 을 통해 job 이 생성된 것 확인 가능
      - 해당 job 의 `COMPLETIONS` 값이 `0/1` 에서 `1/1` 로 되면, `0_pv_output.yaml` 에 작성한 host 의 directory 하위 `{$experiment_id}/` 경로에 output 저장된 것 확인 가능
    