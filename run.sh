kind create cluster --name test --config ./cluster-config.yml 

kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml

docker build -t flask-app ./app 

kubectl apply -f ./secret.yml 

kubectl apply -f ./postgres-deployment.yml

kind load docker-image flask-app --name test   

kubectl apply -f ./flask-deployment.yml  

kubectl apply -f ./ingress.yml