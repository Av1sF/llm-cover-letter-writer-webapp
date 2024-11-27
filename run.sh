kind create cluster --name cloud-cw --config ./k8/cluster-config.yml 

kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml

docker build -t flask-app ./app 

docker build -t llm-model-server ./model_server

kubectl apply -f ./k8/secret.yml 

kubectl apply -f ./k8/postgres-deployment.yml

kind load docker-image llm-model-server --name cloud-cw 

kind load docker-image flask-app --name cloud-cw   

kubectl apply -f ./k8/model-deployment.yml

kubectl apply -f ./k8/flask-deployment.yml  

kubectl apply -f ./k8/ingress.yml
