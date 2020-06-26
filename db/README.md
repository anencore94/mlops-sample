# DB
- mysql image 사용하여 생성

## 요구 사항
- 추후 다른 pod 에서 mysql client 를 사용하기 위해 db, user, password, port 제공 필요
- 특정 table 생성하는 ddl 을 pod init 단계에서 수행 필요

## 구성 요소
- 1_configmap.yaml
  - db initial 할 sql 스크립트 수행하기 위함
- 2_pod.yaml
  - 실제 mysql pod 생성
- 3_svc.yaml
  - mysql pod 의 ip, port 대신 node 의 ip, port 를 사용하여 mysql client 가 접근하기 쉽게 하기 위함

## 생성 방법
```commandline
cd ./db/yaml
kubectl apply -f 1_configmap.yaml
kubectl apply -f 2_pod.yaml
kubectl apply -f 3_svc.yaml
```

## 접속 방법
> mysql client 가 깔려있는 노드 혹은 pod 에서 수행
> 현재 하드코딩된 config 정보는 2_pod.yaml 의 env 에서 확인 가능
- mysql -h {$mysql pod 이 생성된 node의 IP} --port=31111 -u testuser -ptestpassword

## 확인 방법
- mysql bash 에 접속한 후 다음 수행하여 정상 출력되는지 확인
```commandline
mysql> select * from MODEL_INFO;
```

## 이슈
### 1) 한글 깨짐 현상 [해결 완료]
- 다음 링크 참고하여 initialize 시 수행하도록 변경
    - [링크 1](https://nesoy.github.io/articles/2017-05/mysql-UTF8)
    - [링크 2](https://nesoy.github.io/articles/2017-05/mysql-UTF8)
    - 변경 필요한 내용
        ```
        [client]
        default-character-set=utf8
        
        [mysql]
        default-character-set=utf8
        
        
        [mysqld]
        collation-server = utf8_unicode_ci
        init-connect='SET NAMES utf8'
        character-set-server = utf8
        ```
    - mysql pod 의 `/etc/mysql/conf.d/mysql.cnf` ([mysql], [client] 부분) 와 `/etc/mysql/conf.d/docker.cnf` ([mysqld] 부분) 파일 내부 내용 변경 후 mysql service 재시작
- Database, table 생성 전에 수행되어야 함

### 추후 발생할 수도 있는 문제
- 혹시 권한 문제 생길 경우 다음 링크 참고하여 initialize 시 수행하도록 변경 필요 : [링크](https://www.fun25.co.kr/blog/mysql-grant-user-privileges/?page=6)
- 용량 많이 필요한 경우 pvc 생성하여 mount
