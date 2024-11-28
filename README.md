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
4. Once the shell script has finished running you should be able to connect to the application via a browser with http://localhost/ 

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
   ```
4. WAIT until the container `model_server` has finished it's application startup, and connect to the webapp via one of the addresses `flask_app` is currently running on. 

# Usage 
### Webapp GUI Walkthrough 
1. Connect to the Flask webapp via the method specified for your specific method of deploying. (ie, http://localhost/ for Kubernetes)
   ![image](https://github.com/user-attachments/assets/69525335-1ed7-4189-a15e-d52127929670)
2. Click on Register and it should lead you to /auth/register page. 
   ![image](https://github.com/user-attachments/assets/fed5e718-ea5d-4cce-9f63-85403f950b25)
3. 





## Contact
Avis Fung  
K23036967 
avis.cl.fung@kcl.ac.uk 
