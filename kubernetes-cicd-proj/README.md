# How to series
# Kubernetes Deployment

Step 1: Create a server for Jenkins and ansible

    Build
   - t2.micro
   - number instance 2
   - choose your own traffic SG
   - choose your keypair

Step 2: Create a server instances of Kubernetes

    Build
    - t2.medium
    - choose your own traffic SG
    - choose your keypair

Step 3: Rename in the dashboard your instances and hostname

    3.1 Rename the following names
    - jenkins-server
    - ansible-server
    - webapp-server
    3.2 Access first the jenkins-server by getting the public ip address
    3.3 open terminal point in the folder where the keypair and ssh 
    3.4 switch the user to root
    ```
    sudo su
    ```

    3.5 Update and Install the jenkins

    - Follow the installation documents note: In order jenkins will work, install the java
    - Open the public ip address using the browser
    - install the plugin in the starting 

    3.6 Install certain plugins in the jenkins  

        - Click the "Manage Jenkins" and "Manage Plugin"
        - Click the tab "Available"
        - Search "SSH Agent" and "Install without restart"

Step 4: Setup and install the ansible for server instances ansible

    4.1 Switch to the Super User

    ```
    sudo su
    ```

    4.2. Install the ansible usng the documents or use my setup repi in installing ansible


Step 5: Access the Kubernetes cluseter or webapp-server

    5.1 Get the public address and open the terminal to ssh

    5.2 Install the minikube using my repo shell script or follow the steps

    docker
    https://github.com/mgelvoleo/installation-script/blob/main/docker/README.md

    Minikube
    https://github.com/mgelvoleo/installation-script/tree/main/minikube

