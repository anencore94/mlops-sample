# DB
- mysql image 사용하여 MYSQL server 를 pod 으로 생성

## 요구 사항
- 추후 다른 pod 에서 mysql client 로 query 를 수행하기 위해 IP, PORT, user, password, database 의 유연한 제공 필요
  - pod.yaml 의 env 로 명시
  - service 생성
- 특정 table 생성하는 ddl 을 pod init 단계에서 수행 필요
  - pod.yaml 의 configmap 으로 명시
  - configmap.yaml 에서 ddl 작성

## 구성 요소
- 1_configmap.yaml
  - mysql server 초기화 단계에서 기본적인 table 을 create 하는 ddl 수행
  - 한글 입출력을 위해 utf-8 관련 설정
- 2_pod.yaml
  - mysql pod 생성
- 3_svc.yaml
  - mysql pod 의 IP 는 유동적인 값이므로, node 의 ip, port 를 사용하여 mysql client 가 쉽게 접근할 수 있도록 일종의 port-forwarding 역할 수행

## 생성 방법
```commandline
# 순서대로 다음을 실행한다.
cd ./db/yaml
kubectl apply -f 1_configmap.yaml
kubectl apply -f 2_pod.yaml
kubectl apply -f 3_svc.yaml
```

## 접속 방법
> mysql client 가 깔려있는 노드 혹은 pod 에서 수행
> 현재 하드코딩된 config 정보는 2_pod.yaml 의 env 에서 수정 가능
- 예)
  - `mysql -h {$mysql pod 이 생성된 node의 IP} --port=31111 -u testuser -ptestpassword -D testdb`

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
