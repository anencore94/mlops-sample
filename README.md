# mlops-sample
End to End MLops 샘플 in k8s cluster

## 구성
- kubecluster 내부에 각각의 구성 요소가 각각 pod 으로 생성되어 서로 통신하는 상황을 가정합니다.
    - DB : mysql
    - Backend Server : flask
    - Frontend Server : react-app
    - ML model : 특정 argument 를 받아 `*.py` 파일을 실행하는 docker image 로 생성된 pod

