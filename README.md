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


   











## Contact
Avis Fung  
K23036967 
avis.cl.fung@kcl.ac.uk 
