# Cover Letter Writer (5CCSACCA Coursework)

# Project Overview
### Problem Description 
As the recruitment season is in full swing, informatic students are actively seeking industrial placements, internships, and graduate opportunities. A significant challenge they face in this tenacious process is crafting targeted cover letters; a task often regarded as both time-consuming and labour-intensive. To address these challenges, the proposed Software-as-a-Service (SaaS) solution will be a single-tenant vertical web application with authenticated access. The web-application will generate personalised cover letters that incorporate technical and soft skills, linking these to the students' relevant experience.  

### Built With
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Starlette](https://www.starlette.io/)
- [MLflow](https://mlflow.org/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)
- [Kind](https://kind.sigs.k8s.io/)
- [Kubernetes](https://kubernetes.io/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Transformers](https://github.com/huggingface/transformers)
- [Pytorch](https://pytorch.org/)

To give a brief overview on deployment, the application is able to be deployed with Docker Compose and Kind clusters. The foundation of both architectures relies on 3 main containers: the Flask server, the Postgres database, and a Starlette server to handle queries to the model. 

Docker Compose was used as part of the development process for proof of concept and a learning step to ensure communications between containers was possible before scaling it with Kind Kubernetes. Kubernetes, was chosen to scale the application, due to it's infrastructure abstraction and automated service monitoring. Kind's Docker-based container runtime approach allowed faster start up time, ease of testing, and ensured successful deployment of k8s clusters locally. 

### Challenges and Potential Feature Implementations 
- Quick inference times due to CPU and RAM limitations (average inference is 4 minutes)
- Fine-tuning LLM Model weights due to model size and limitations with CPU 
- Implementing a infrastructure that would not overwhelm the LLM model. 
- Could implement a save function that will save generated model outputs to user's account, improving user experience. 

# Getting Started 
## Prerequisites 
- [Kind]("https://kind.sigs.k8s.io/docs/user/quick-start")
- [Kubectl]("https://kubernetes.io/docs/tasks/tools/")
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  Docker Desktop allows for an efficient GUI, it also installs Docker and Docker Compose together to remove the hassle of installing it seperately. If you choose to deploy the application via Kubernetes, there is no need for Docker Compose. Hence, you could choose to download Docker as a standalone [here](https://docs.docker.com/engine/install/). 

## Installation on Linux 
1. Clone the repo 
   ```
   git clone https://github.com/5CCSACCA/coursework-Av1sF.git
   ```
   Then you can either deploy with [kubernetes](#deploying-with-kind-kubernetes) or [Docker Compose](#deploying-with-docker-compose)

## Deploying with Kind Kubernetes 
1. Ensure you are currently in the project directory 
   ```
   cd ./path/to/project/dir/coursework-Av1sF
   ```
2. Make sure that you have execute permissions for `deploy-in-k8s.sh` and all yaml files in the `k8` directory. You can change all the files in the project directory have all permissions types with this command below. 
   ```
   chmod -R 777 ./
   ```
3. Run the shell script
   ```
    ./deploy-in-k8s.sh 
   ```
4. Once the shell script has finished running you should be able to connect to the application via a browser with http://localhost/. Here is a snippet of what the first and last few lines of output should be from the script.
   ```
   $ sh deploy-in-k8s.sh
    ***5CCSACCA ~ Avis Fung k23036967 avis.cl.fung@kcl.ac.uk***
    ***KUBERNETES DEPLOYMENT***
    
    ***Creating kind cluster with name cloud-cw and specified configs***
    Creating cluster "cloud-cw" ...
     • Ensuring node image (kindest/node:v1.31.2) 🖼  ...
     ✓ Ensuring node image (kindest/node:v1.31.2) 🖼
     • Preparing nodes 📦   ...
     ✓ Preparing nodes 📦 
     • Writing configuration 📜  ...
     ✓ Writing configuration 📜
     • Starting control-plane 🕹️  ...
     ✓ Starting control-plane 🕹️
     • Installing CNI 🔌  ...
    ...
    ...
    ...
    ***Kubernetes Metrics Server for Kind***
    serviceaccount/metrics-server created
    clusterrole.rbac.authorization.k8s.io/system:aggregated-metrics-reader created
    clusterrole.rbac.authorization.k8s.io/system:metrics-server created
    rolebinding.rbac.authorization.k8s.io/metrics-server-auth-reader created
    clusterrolebinding.rbac.authorization.k8s.io/metrics-server:system:auth-delegator created
    clusterrolebinding.rbac.authorization.k8s.io/system:metrics-server created
    service/metrics-server created
    deployment.apps/metrics-server created
    apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io created
    deployment.apps/metrics-server patched
    
    *** You can now connect to the webapp through http://localhost/ ***
    *** To delete cluster: kind delete cluster --name cloud-cw ***
   ```

## Deploying with Docker Compose 
1. Ensure you are currently in the project directory 
   ```
   cd ./path/to/project/dir/coursework-Av1sF
   ```
2. Make sure that you have execute permissions for `deploy-in-docker-compose.sh` and all Docker files. You can change all the files in the project directory have all permissions types with this command below. 
   ```
   chmod -R 777 ./
   ```
3. Run the shell script 
   ```
    ./deploy-in-docker-compose.sh

   ***5CCSACCA ~ Avis Fung k23036967 avis.cl.fung@kcl.ac.uk***
    ***DOCKER COMPOSE DEPLOYMENT***
    
    ***Please wait container model_server to be loaded before connecting to the flask app***
    ***Flask app can be connected via all 0.0.0.0 address via port 5000***
    
    
    [+] Building 1.1s (23/23) FINISHED                                                           docker:desktop-linux
     => [model_server internal] load build definition from Dockerfile                                            0.0s
     => => transferring dockerfile: 264B                                                                         0.0s
   ...
   ...
   ...

    flask_db      | 2024-11-28 05:09:00.262 UTC [28] LOG:  database system was shut down at 2024-11-27 18:15:26 UTC   
    flask_db      | 2024-11-28 05:09:00.277 UTC [1] LOG:  database system is ready to accept connections
    flask_app     |  * Serving Flask app 'app'
    flask_app     |  * Debug mode: off
    flask_app     | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.                                                                                              
    flask_app     |  * Running on all addresses (0.0.0.0)
    flask_app     |  * Running on http://127.0.0.1:5000                                                               
    flask_app     |  * Running on http://172.21.0.4:5000
    flask_app     | Press CTRL+C to quit                                                                              
    model_server  | ***Qwen2.5-0.5B-Instruct Model Loaded in Locally***
    model_server  | ***Qwen2.5-0.5B-Instruct LLM model Initalised***
    model_server  | INFO:     Started server process [1]                                                              
    model_server  | INFO:     Waiting for application startup.
    model_server  | INFO:     Application startup complete.
    model_server  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)                                               
   ```
4. WAIT until the container `model_server` has finished it's application startup, and connect to the webapp via one of the addresses `flask_app` is currently running on.
5. To stop, CTRL+C and then run `docker compose down`

# Usage 
Consist of 3 main parts: [cURL Walkthrough](#curl-walkthrough), [Webapp GUI Walkthrough](#webapp-gui-walkthrough) and [Kubernetes Metrics Commands](#kubernetes-metrics-commands)
## cURL Walkthrough 
In this walkthrough, I will be using the Kubernetes deployment so the URL will be 'localhost'. If you are using Docker Compose deployment, the URL should be listed in `flask_app` container logs (ie. http://127.0.0.1:5000).
1. Retrieve main landing page. It should return index.html. 
   ```
   $ curl localhost
   <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Cover Letter Writer. </title>
   ...
   ```
2. Retrieve registration.html
   ```
    $ curl -X GET http://localhost/auth/register
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Register</title>
    ...
   ```
3. Create your user account
   ```
    $ curl -X POST http://localhost/auth/register \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -d "username=foo&password=Bar2024%21&email=foobar%40gmail%2Ecom"
   ```
   If you have encoded a valid email, along with a password that:
   - minimum eight characters
   - at least one uppercase letter
   - one lowercase letter
   - one number
   - one special character  
  Then the response html should contain a message that states `Created user successfully`,  otherwise it would display the appropriate user input error message.  
4. Log in to your registered account.  
   GET method returns the login.html
   ```
    $ curl -X GET localhost/auth/login 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Login</title>
   ...
   ```
   Log in to your account and also retrieve our access tokens. Should return redirect message, if login is successful. An HTML page will be returned with an error message, if the login is unsuccessful. 
   ```
   $ curl --cookie-jar cookies.txt -X POST http://localhost/auth/login \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -d "username=foo&password=Bar2024%21"

   
   <!doctype html>
    <html lang=en>
    <title>Redirecting...</title>
    <h1>Redirecting...</h1>
    <p>You should be redirected automatically to the target URL: <a href="/user/protected">/user/protected</a>. If not, click the link.
   ```
   When this is executed, it will save the tokens which are stored in Cookies in a text file called `cookies.txt` in your current directory:
   ```
   # Netscape HTTP Cookie File
   # https://curl.se/docs/http-cookies.html
   # This file was generated by libcurl! Edit at your own risk.
    
    localhost	FALSE	/	TRUE	0	csrf_access_token	f798479e-5129-48f9-af86-5b0f55e35685
    #HttpOnly_localhost	FALSE	/	TRUE	0	access_token_cookie	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjc2MzE5MSwianRpIjoiNzA0YjFmMWUtMzFjNy00NTQ4LWJiMGYtYjNmODdmZGYxZDQwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3MzI3NjMxOTEsImNzcmYiOiJmNzk4NDc5ZS01MTI5LTQ4ZjktYWY4Ni01YjBmNTVlMzU2ODUiLCJleHAiOjE3MzI3NjY3OTF9.YhyOPFxRVGCRaelKgiFdCPKjT0WX1RZAO8tHMOp0Zcc
   ```
   Keep ahold of these! As we will need them later.
6. To access our protected root, go to your cookies.txt and copy the unique `access_token_cookie` like so... 
   ```
   $ curl -b "access_token_cookie=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjc2MzE5MSwianRpIjoiNzA0YjFmMWUtMzFjNy00NTQ4LWJiMGYtYjNmODdmZGYxZDQwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3MzI3NjMxOTEsImNzcmYiOiJmNzk4NDc5ZS01MTI5LTQ4ZjktYWY4Ni01YjBmNTVlMzU2ODUiLCJleHAiOjE3MzI3NjY3OTF9.YhyOPFxRVGCRaelKgiFdCPKjT0WX1RZAO8tHMOp0Zcc" \
    http://localhost/user/protected

   
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Cover Letter Writer.</title>
    
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/static/css/styles.css">
    
              <!-- fonts -->
              <link rel="preconnect" href="https://fonts.googleapis.com">
              <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
              <link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,100..900;1,100..900&family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap" rel="stylesheet">
        </head>
    
        <body>
            <!-- Toolbar -->
            <div class="container">
                    <div class="container">
                        <h1>Cover Letter Writer.</h1>
                    </div>
    
                    <div class="container">
                        <a class="btn" href="/user/profile">
                            View Profile

   ```
   We know we have successfully accessed the protected page, when it has a 'View Profile button' in the response. If the curl command does not feature a valid access token, an error response could be `{"msg":"Missing cookie \"access_token_cookie\""}`
7.  Updating user data. With POST requests, we also need to include our CSRF Token in our headers. Hence, go to your cookies.txt and copy the unique `access_token_cookie` and `csrf_access_token` like so...
   ```
    $ curl -X PUT http://localhost/user/update -b \
"access_token_cookie=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjc2MzE5MSwianRpIjoiNzA0YjFmMWUtMzFjNy00NTQ4LWJiMGYtYjNmODdmZGYxZDQwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3MzI3NjMxOTEsImNzcmYiOiJmNzk4NDc5ZS01MTI5LTQ4ZjktYWY4Ni01YjBmNTVlMzU2ODUiLCJleHAiOjE3MzI3NjY3OTF9.YhyOPFxRVGCRaelKgiFdCPKjT0WX1RZAO8tHMOp0Zcc" \
-H "Content-Type: application/x-www-form-urlencoded" -H "X-CSRF-TOKEN:f798479e-5129-48f9-af86-5b0f55e35685" \
-d "username=foo&email=foobar%40gmail%2Ecoem"
    
    {"updateMsg":"User information updated."}
   ```
9.  Querying the LLM Model. This one is really long, so I have put {placeholders} to denote where you should put your token values
   ```
    $ curl -F 'Job Title=Data Scientist' -F 'Preferred Qualifications=4 years experience machine learning' \
-F 'Hiring Company=google' -F 'Applicant Name=John' -F 'Past Working Experience=Machine Learning Intern at Sony' \
 -F 'Current Working Experience=Analyst at Trello' -F 'Skillsets=python' \
-F 'Qualifications=BSc in Computer Science' \
 -H 'Content-Type: multipart/form-data' http://localhost/model/query \
 -b "access_token_cookie={access_token_cookie}" -H "X-CSRF-TOKEN:{csrf_access_token}"

{"modelOutput":"Dear Hiring Manager,\n\nI am writing to express my strong interest in the Data Scientist position at Google, and I believe that my skills and qualifications align perfectly with the requirements of this role.\n\nAs an experienced data scientist with a track record of 4 years of experience in machine learning, I bring a unique perspective on how to apply these skills effectively in a professional setting. My past work experiences include roles as a Machine Learning Intern at Sony, where I honed my abilities in developing and implementing machine learning algorithms; and as an Analyst at Trello, where I utilized my analytical skills to identify trends and opportunities for growth within our company.\n\nIn addition to my technical expertise, I possess excellent communication and collaboration skills, which make me a valuable asset to any team. My passion for data science has led me to pursue further education and certification in Python programming, ensuring that I can continue to develop and enhance my skills in this field.\n\nMy current employment history includes working as an analyst at Trello, where I have consistently contributed to project management and strategic planning. I am confident that my ability to analyze complex data sets and present insights to stakeholders will be a valuable asset to your team.\n\nThank you for considering my application. I look forward to the opportunity to discuss how my background and skills could benefit your organization.\n\nSincerely,\nJohn"}
   ```  
10.  Delete user  
    ```
    $ curl -X DELETE http://localhost/user/delete \
    -b "access_token_cookie={access_token_cookie}" -H "X-CSRF-TOKEN:{csrf_access_token}"  
    ```
12. Log out (redirect response)
    ```
    $ curl -X POST http://localhost/auth/logout

    <!doctype html>
    <html lang=en>
    <title>Redirecting...</title>
    <h1>Redirecting...</h1>
    <p>You should be redirected automatically to the target URL: <a href="/">/</a>. If not, click the link.
    ```

## Webapp GUI Walkthrough 
1. Connect to the Flask webapp via the method specified for your specific method of deploying (ie, http://localhost/ for Kubernetes)
   ![image](https://github.com/user-attachments/assets/69525335-1ed7-4189-a15e-d52127929670)
2. Click on Register and it should lead you to /auth/register page
   ![image](https://github.com/user-attachments/assets/fed5e718-ea5d-4cce-9f63-85403f950b25)
3. Create a user. When successful it should show you this message on screen
   ![image](https://github.com/user-attachments/assets/34c3fb65-8cf0-42f4-8692-6c726a30c8d2)
4. Go to the login (/auth/login) page and login with the credentials you just used to register
   ![image](https://github.com/user-attachments/assets/8021063d-aa11-4cdf-9072-ecdf30884ff7)
5. You should be redirected to /user/protected where you can query the model!
   ![image](https://github.com/user-attachments/assets/b1154432-fd46-4e64-836d-7fb4004762e9)
6. Enter meaningful work experiences with statistics along with soft/technical skills and submit the form by pressing 'Generate!'
   ![image](https://github.com/user-attachments/assets/1fb67a55-317d-4c48-97bc-67226708b497)
7. Wait patiently, the inference time depends on your CPU.
   ![image](https://github.com/user-attachments/assets/59a37a63-8cb2-4269-acd4-917133f5765f)
8. To logout you can click the top right button 'logout', which should log you out and redirect you to the main page (/)
9. To view your profile information, click the top right button 'View Profile'
    ![image](https://github.com/user-attachments/assets/5e897bc2-f164-4c70-9e3b-1621ec99915a)
10. To change your profile details, edit your username and/or email and click 'update'. The page should now display your updated info.
    ![image](https://github.com/user-attachments/assets/b8e0601b-1713-4604-b7e5-889ba6bb84f9)
11. To delete your profile, press the delete button and it should redirect you to the main page (/). The login credentials will now not work.
    ![image](https://github.com/user-attachments/assets/41330f6f-75b9-48cc-867b-d1260b7339f7)


## Kubernetes Metrics Commands 
As the metrics server is automatically deployed in the cluster, it can be used for monitoring. Here are some useful commands!  
```
$ kubectl top node
NAME                     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
cloud-cw-control-plane   397m         3%     2228Mi          14%  
```
```
$ kubectl top pod -A
NAMESPACE            NAME                                             CPU(cores)   MEMORY(bytes)   
default              flask-555849dd57-4p6gq                           1m           50Mi
default              flask-555849dd57-fz5g6                           1m           53Mi
default              llm-model-7fd4ddb5bd-g8xkj                       4m           584Mi
default              postgres-6b5f7d7849-wk22n                        1m           36Mi
ingress-nginx        ingress-nginx-controller-5f4f4d9787-n8jd6        4m           149Mi
kube-system          coredns-7c65d6cfc9-5j2v9                         5m           20Mi
kube-system          coredns-7c65d6cfc9-gvs9x                         6m           19Mi
kube-system          etcd-cloud-cw-control-plane                      62m          51Mi
kube-system          kindnet-rrfsb                                    2m           15Mi
kube-system          kube-apiserver-cloud-cw-control-plane            102m         220Mi
kube-system          kube-controller-manager-cloud-cw-control-plane   49m          60Mi
kube-system          kube-proxy-q2mwb                                 2m           21Mi
kube-system          kube-scheduler-cloud-cw-control-plane            9m           23Mi
kube-system          metrics-server-56d84f4d65-7c99f                  8m           30Mi
local-path-storage   local-path-provisioner-57c5987fd4-k79c4          2m           14Mi
```
```
$ kubectl describe node
```
   











## Contact
Avis Fung  
K23036967 
avis.cl.fung@kcl.ac.uk 
