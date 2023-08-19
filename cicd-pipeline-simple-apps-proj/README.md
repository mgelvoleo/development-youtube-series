# CICD Project (Github,Jenkins, Docker)


## Here's a step-by-step guide for your project on setting up a CI/CD pipeline using GitHub, Jenkins, and Docker:

![Some things you should know about me (13)](https://github.com/mgelvoleo/development-youtube-series/assets/21300768/1bfdfd20-d7ec-4aa5-917c-5ca7f4a77061)


### Step 1: Create an EC2 Instance Set up an Amazon EC2 instance to host your Jenkins server and your web application. Make sure to configure security groups, access keys, and other necessary settings.

### Step 2: Install Jenkins and Docker on Jenkins Server

SSH into your Jenkins server.Install Jenkins by following my repo.

https://github.com/mgelvoleo/installation-script/tree/main/jenkinsRestart Jenkins to apply changes: sudo systemctl restart jenkins.

### Step 3: Install Docker on Web App Server

SSH into your web app server.Install Docker using my repo
https://github.com/mgelvoleo/installation-script/tree/main/docker

### Step 4: Install SSH Agent Plugin in Jenkins

In the Jenkins dashboard, go to "Manage Jenkins" > "Manage Plugins."Search for "SSH Agent Plugin" and install it.This plugin will allow you to use SSH keys for authentication in your pipeline.

### Step 5: Create a Pipeline in Jenkins

In the Jenkins dashboard, click on "New Item."Choose "Pipeline" and provide a name for your pipeline.Under the "Pipeline" section, select "Pipeline script from SCM."Choose "Git" as the SCM and provide your GitHub repository URL.Specify the script path if necessary (e.g., Jenkinsfile).

### Step 6: Define Stages in Your Jenkinsfile Here's a simplified example of the stages in your Jenkinsfile:
```
node {
   stage('Git Checkout') {
       git branch: 'main', url: 'https://github.com/mgelvoleo/docker-jenkins-proj.git'
   }

   stage('Docker build image') {
       def imageName = "${JOB_NAME}:${BUILD_ID}"
       sh "docker build -t ${imageName} ."
       sh "docker tag ${imageName} mgelvoleo/${imageName}"
   }

   stage('Pushing images to Dockerhub') {
       withCredentials([string(credentialsId: 'DockerPasswd', variable: 'DockerPasswd')]) {
           sh "docker login -u mgelvoleo -p ${DockerPasswd}"
           def imageName = "${JOB_NAME}:${BUILD_ID}"
           sh "docker push mgelvoleo/${imageName}"
           sh "docker rmi mgelvoleo/${imageName}"
       }
   }

   stage('Docker container deployment') {
       def remoteHost = 'ubuntu@172.31.28.40'
       def containerName = 'container-name'
       sshagent(['webapp-server']) {
           sh "ssh -o StrictHostkeyChecking=no ${remoteHost} 'docker rm -f ${containerName} || true'"
           sh "ssh -o StrictHostkeyChecking=no ${remoteHost} 'docker run -itd --name ${containerName} -p 9000:80 mgelvoleo/${JOB_NAME}:${BUILD_ID}'"
       }
   }
}

```

### Step 7: Run Your Pipeline After defining your pipeline stages, save the Jenkinsfile and trigger the pipeline manually or configure it to be triggered on code changes.

Remember, this is a high-level overview of the steps involved in creating your CI/CD pipeline. Depending on your specific environment and requirements, you might need to adjust configurations and scripts accordingly. Happy automating! 🚀🌐
 
