# 개인 저장용 cmd
## minikube start with insecure-registry
 ```commandline
 ~/git/minikube/out/minikube start --kubernetes-version=v1.16.3 --insecure-registry "192.1.4.75:5000"
```

## repository 에 image 확인
```commandline
curl -X GET http://localhost:5000/v2/_catalog
curl -X GET http://localhost:5000/v2/hello-flask/tags/list
```

## flask pod 확인
> 
```commandline
curl -X GET $(~/git/minikube/out/minikube ip):31112
```

## flask pod 다시 빌드해서 pod 새로 띄우기
```commandline
/home/kjy/git/mlops-sample/backend/build.sh && kubectl delete -f yaml/3_pod.yaml && kubectl apply -f yaml/3_pod.yaml
```

## docker container 접속
```commandline
docker exec -it {$docker container id} /bin/bash
```