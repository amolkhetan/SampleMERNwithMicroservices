# Sample MERN with Microservices


**Step By Step Execution**

**1. Set Up AWS CLI and Boto3**

   Run "msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi" to install AWS CLI in not present on your machine
   Run "aws –version" to check version

   <img width="940" height="127" alt="image" src="https://github.com/user-attachments/assets/c465a4a8-6e60-4a19-99c9-9598b8d82b58" />

   Run "pip install boto3" to install boto3
   Run "python -c "import boto3; print(boto3.__version__)"" to verify if already installed

   <img width="940" height="69" alt="image" src="https://github.com/user-attachments/assets/49f8c1fd-4813-43b7-aabd-ff5835ee32ea" />

**Step 2: Prepare the MERN Application**
Clone the Repo using "Git clone https://github.com/amolkhetan/SampleMERNwithMicroservices.git"
Create Dockerfiles for 2 backend and one frontend service (Refer Repo for Dockerfiles)

For `helloService`, create `.env` file with the content:
```bash
PORT=3001
```

For `profileService`, create `.env` file with the content:
```bash
PORT=3002
MONGO_URL="specifyYourMongoURLHereWithDatabaseNameInTheEnd"
```

Finally install packages in both the services by running the command `npm install`.

<br/>
For frontend, you have to install and start the frontend server:

```bash
cd frontend
npm install
npm start
```

Docker Build Command

docker build -t amolkhetan/helloservice .
docker build -t amolkhetan/profileservice .
docker build -t amolkhetan/frontend .

Docker Run Command

docker run -p 3001:3001 amolkhetan/helloservice
docker run -p 3002:3002 amolkhetan/profileservice
docker run -p 3000:3000 amolkhetan/fronend

Local Testing

<img width="940" height="267" alt="image" src="https://github.com/user-attachments/assets/5055a1a1-96ee-4f0d-99ae-8630a057bca6" />

<img width="940" height="177" alt="image" src="https://github.com/user-attachments/assets/9b2da3f2-96f9-4c61-9ec2-028a32cad001" />

<img width="940" height="165" alt="image" src="https://github.com/user-attachments/assets/7df8b6dd-209a-408b-99e9-d11d2b974f63" />


Login to ECR and push images:

Login to ecr 

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 975050024946.dkr.ecr.us-west-2.amazonaws.com

docker tag amolkhetan/mern-helloservice 975050024946.dkr.ecr.us-west-2.amazonaws.com/amolkhetan/helloservice:latest
docker tag amolkhetan/mern-profileservice 975050024946.dkr.ecr.us-west-2.amazonaws.com/amolkhetan/profileservice:latest
docker tag amolkhetan/mern-frontservice 975050024946.dkr.ecr.us-west-2.amazonaws.com/amolkhetan/frontend:latest

**Step 3: Version Control**
Since CodeCommit is no more active/applicable for new users, used github as SCM solution.
<img width="940" height="246" alt="image" src="https://github.com/user-attachments/assets/663467e5-c8e6-41db-b7b8-f899f16358a9" />


**Step 4: Continuous Integration with Jenkins**
**Set Up Jenkins:**
Launch EC2 Instance and below command once you connect to instance using EC2 instance connect to putty:

Install Java (required for Jenkins):
sudo apt update 
#Java to be installed for Jenkins as it is java based application 
sudo apt install openjdk-17-jdk -y

# 1. Download and store the Jenkins GPG key
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

# 2. Add the Jenkins repo using the keyring
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# 3. Update package list
sudo apt update

# 4. Install Jenkins
sudo apt install jenkins -y

Note: Enable security greoup to open port 8080

<img width="940" height="476" alt="image" src="https://github.com/user-attachments/assets/552e97d8-8844-49f7-9d24-d7e36be3ec38" />

Initial Password can be found using "sudo cat /var/lib/jenkins/secrets/initialAdminPassword"

<img width="940" height="470" alt="image" src="https://github.com/user-attachments/assets/886caa79-3b94-43eb-9da5-ffd946a0260c" />
<img width="940" height="463" alt="image" src="https://github.com/user-attachments/assets/ccaa23c4-38f5-4fe7-a494-9b6454576e41" />
<img width="940" height="481" alt="image" src="https://github.com/user-attachments/assets/b15e2ba1-5c73-4134-84ae-3c3dfdeeb4ae" />


Now, create a script to build and push images to ECR and it should trigger whenever code changes in git.
This is achived by using polling:
<img width="940" height="392" alt="image" src="https://github.com/user-attachments/assets/d622702b-4948-48b0-bd4a-7cfd28e66d43" />

Groovy script is present in repo and console output is also attached as supporting doc to show it is auto triggered and uploading images to ecr.


**Step 5: Infrastructure as Code (IaC) with Boto3**
IaC.py file is added in repo to create VPC, subnets, security groups

Below are few screenshots to showcase same:
<img width="940" height="379" alt="image" src="https://github.com/user-attachments/assets/33a5815c-9c06-492c-86c7-9280a4dcd538" />
<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/12af1a48-97b5-4b96-b85b-7e6a7541050e" />
<img width="940" height="505" alt="image" src="https://github.com/user-attachments/assets/c5cf194a-f7b4-4f1f-bfc5-8347b66d8e24" />

**Step 6: Deploying Backend Services**
DeployBackend.py is added in repo for backend deployment using boto3 

<img width="940" height="327" alt="image" src="https://github.com/user-attachments/assets/4153a781-97a7-4850-951c-87049b781271" />
<img width="940" height="327" alt="image" src="https://github.com/user-attachments/assets/18efa89b-ef3c-4dc7-9fff-37fbff790192" />
<img width="940" height="481" alt="image" src="https://github.com/user-attachments/assets/0f0fe4d0-536a-4d43-bd07-77036174f755" />
<img width="940" height="496" alt="image" src="https://github.com/user-attachments/assets/94e8a7e0-6664-45f6-b1cc-fdcce18aa26f" />
<img width="940" height="501" alt="image" src="https://github.com/user-attachments/assets/1b402f6b-cb35-43e2-adce-9ca28b538967" />

**Step 7: Set Up Networking**













Note: This will run the frontend in the development server. To run in production, build the application by running the command `npm run build`
