# mlops-sample
End to End MLops 샘플 in k8s cluster

## 구성
- k8s cluster 내부에 각각의 구성 요소가 pod 으로 생성되어 서로 통신할 수 있는 상황을 가정합니다.
    - DB : mysql
    - datasets : data 저장 경로 (pvc 로 제공)
    - Backend Server : flask
    - Frontend Server : react-app
    - ML model : 특정 argument 를 받아 `*.py` 파일을 실행하는 docker image 로 생성된 pod

### Quick Start
- docker registry 구축
  - 해당 docker registry 에 flak, ml_model docker image push
- kube 환경 구축 (node 1개가 아닐 경우 내부 수정 필요)
  - kube 환경에서 해당 docker registry 를 insecure-registry 로 설정
- mysql server 구축
  - `kubectl apply -f {mlops-sample/db/yaml/*.yaml` 순서대로 수행
  - mysql pod 이 running 인지 확인
- flask server 구축
  - `kubectl apply -f {mlops-sample/backend/yaml/*.yaml}` 순서대로 수행
  - flask pod 이 running 인지 확인
- flask api 날리기
  - `hello flask` api 가 정상적으로 날아가는지 확인
  - `ml_model` api 날리기
    - ml_model job 이 생성되고 completed 되었는지 확인
    - 정해진 경로에 output 이 정상적으로 저장되었는지 확인
- (TODO) react-app server 에서 page 생성하여 flask api 를 버튼클릭으로 날릴 수 있게 구현