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
  - `./backend/build.sh`, `./ml_model/autoencoder/build.sh` 수행
    - **두 build.sh 파일 내 registry URL 수정 후 실행**
- kube 환경 구축 (node 1개가 아닐 경우 내부 수정 필요)
  - kube 환경에서 해당 docker registry 를 insecure-registry 로 설정
  - 검색하면 나옴
    - 간단 테스트용으로는 `minikube start --kubernetes-version=v1.16.3 --insecure-registry "192.1.4.75:5000"` 수행하면 자동 설정된 k8s 환경 구축됨
- mysql server 구축
  - `db/README.md` 참고
  - mysql pod 이 running 인지 확인
- flask server 구축
  - `backend/README.md` 참고
  - flask pod 이 running 인지 확인
- 정상 동작 확인
  - `backend/README.md` 참고
  - 정해놓은 경로(0_pv_output.yaml 에 작성한 경로)하위에 output 이 정상적으로 저장되었는지 확인
- (TODO) react-app server 에서 page 생성하여 flask api 를 버튼클릭으로 날릴 수 있게 구현