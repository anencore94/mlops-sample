# mlops-sample
End to End MLops 샘플 in k8s cluster

## 구성
- kubecluster 내부에 각각의 구성 요소가 각각 pod 으로 생성되어 서로 통신하는 상황을 가정합니다.
    - DB : mysql
    - Backend Server : flask
    - Frontend Server : react-app
    - ML model : 특정 argument 를 받아 `*.py` 파일을 실행하는 docker image 로 생성된 pod

### 구현 순서
- mysql pod생성
- flask pod 생성
- flask pod 에서 db 와 connection 하는 api 추가
  - https://github.com/PyMySQL/PyMySQL
  - https://woolbro.tistory.com/91
- ml model pod 생성
  - 우선 arg 2개 받아서 그대로 출력하는 python code 
- flask 에 ml model pod 생성하고 response 받는 api 추가
  