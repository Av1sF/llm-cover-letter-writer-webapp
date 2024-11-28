#!/bin/bash
printf '***5CCSACCA ~ Avis Fung k23036967 avis.cl.fung@kcl.ac.uk***\n'
printf '***KUBERNETES DEPLOYMENT***\n\n'

printf '***Creating kind cluster with name 'cloud-cw' and specified configs***\n' 
kind create cluster --name cloud-cw --config ./k8/cluster-config.yml 


printf '\n\n***Setting up ingress for Kind***\n'
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
# wait until it is readty to process requests 
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s 


printf '\n\n***Building Docker Images***\n'
docker build -t flask-app ./app 
docker build -t llm-model-server ./model_server


printf '\n\n***Deploying Postgres Database in Cluster***\n'
kubectl apply -f ./k8/secret.yml 
kubectl apply -f ./k8/postgres-deployment.yml
# wait until postgres pod's status is Running
kubectl wait --for=jsonpath='{.status.phase}'=Running pod/$(kubectl get pod -l app=postgres -o jsonpath="{.items[0].metadata.name}") --timeout=180s


printf '\n\n***Loading in Docker Images into Kind***\n'
kind load docker-image llm-model-server --name cloud-cw 
kind load docker-image flask-app --name cloud-cw   


printf '\n\n***Deploying LLM Model Server in Cluster***\n'
kubectl apply -f ./k8/model-deployment.yml
# wait until model-server pod's status is Running 
kubectl wait --for=jsonpath='{.status.phase}'=Running pod/$(kubectl get pod -l app=llm-model -o jsonpath="{.items[0].metadata.name}") --timeout=300s
# wait until the pod's logs show that the model has been downloaded and initalised
until kubectl logs $(kubectl get pod -l app=llm-model -o jsonpath="{.items[0].metadata.name}")| grep -m 1 "***Qwen2.5-0.5B-Instruct LLM model Initalised***" ; do sleep 1 ; done

printf '\n\n***Deploying Flask Server in Cluster***\n'
kubectl apply -f ./k8/flask-deployment.yml  
# wait until flask pod's status is running 
kubectl wait --for=jsonpath='{.status.phase}'=Running pod/$(kubectl get pod -l app=flask -o jsonpath="{.items[0].metadata.name}") --timeout=300s
# # wait until the pod's logs show that the flask startup is completed 
until kubectl logs $(kubectl get pod -l app=flask -o jsonpath="{.items[0].metadata.name}")| grep -m 1 "* Serving Flask app 'app'" ; do sleep 1 ; done

printf '\n\n\n***Deploying Ingress Resource Definition***\n'
kubectl apply -f ./k8/ingress.yml

printf '\n\n***Kubernetes Metrics Server for Kind***\n'
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.5.0/components.yaml
kubectl patch deployment metrics-server -n kube-system --patch "$(cat ./k8/metric-server-patch.yml)"


printf '\n\n\n*** You can now connect to the webapp through http://localhost/ ***\n'
printf '*** To delete cluster: kind delete cluster --name cloud-cw ***\n'
