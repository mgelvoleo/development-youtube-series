# How to series
# Project CICD

## SETUP and install the Jenkins Server

STEP 1: Create Instances 

Name: Jenkins
AMI : Amazon Linux 2 AMIA
Keypair: OK
SG: OK note: what is default


STEP 2: Open your favorite xterm

Copy the  public address
point your private key
ok

STEP 3: Access Root
```
sudo su
```
 

STEP 4: get the step for installing jenkins

https://www.jenkins.io/doc/book/installing/linux/

Note: Our distro here is amazon 

STEP 5: Change the hostname of the server

```
 hostnamectl set-hostname jenkins-server
```

STEP 6: Check if port 8080 is open in our Security Group in AWS.

STEP 7: Copy the public address, paste it in the browser, and add port 8080 at the end.

STEP 8: Install the jenkins plugins. provide the information of the users



## Install and configure the Maven

*  Where going to use the jenkins server for install and setup maven

STEP 1. open the url of https://maven.apache.org/install.html, find the download links and copy the binary. Note: In downloading neet to be in root

STEP 2. Getht the binary

```
cd /tmp
wget https://dlcdn.apache.org/maven/maven-3/3.9.3/binaries/apache-maven-3.9.3-bin.tar.gz
tar -xvf apache-maven-3.9.3-bin.tar.gz
mv apache-maven-3.9.3 /opt/maven
```

STEP 3: Add bin for maven in our .bash_profile 

```
~/.bash_profile
```

at the bottom, add this line

M2_HOME=/opt/maven
M2=/opt/maven/bin
JAVA_HOME=/usr/lib/java-11-openjdk-11.0.19.0.7-1.amzn2.0.1.x86_64  note: find / -name java-11*

PATH=$PATH:$HOME/bin:$JAVA_HOME:$M2_HOME:$M2

Save and exit

Reboot the source

```
source .bash_profile
```

## Install Maven Plugin and configure Jenkins for Maven

### Step 1: Go back to the Jenkins Server access the public address and login

### Step 2: Click the Manage Jenkins

    - Click Plugins
        - Avalable plugins
        - Search "maven integration"
        - Install without restart

### Step 3: Go back to Manage Jenkins

    - Click Tools
        - JDK 
            - Click the "Add JDK" and provide the info
                - Name: java11
                - JAVA_HOME: /usr/lib/jvm/java-11-openjdk-11.0.19.0.7.amzn2.0.1.x86_64

        - Maven
            - Maven installations
                - Click "Add Maven" and provide info
                    - Name: maven
                    - un tick Install automatically "install from apache"
                    - MAVEN_HOME: /opt/maven
                - Click apply and save    
### Step 3: Go back to Manage Jenkins

    - Click Plugins
        - Install Plugin
            - Search plugin : github
                - Disable "Github branch Source Plugin"
                - Enable "Github plugin"
            - click Restart Once no job are running

Note: While restarting go to the terminal install the git in the jenkins because amazon linux by default not install

### Stap 4: Access the server

```
yum install git
```

### Step 5: Login again in our Jenkins admin and start create new Item

    - Click "New Item" give the info
        Item Name: Maven-Builder
        Select: Maven project and OK
        Description: Test Maven Build

        Source Code: Git
            Repositories URL: http://github.com/sample/apps
            Brances: main note: depend what you make a default of brances

        Build:
            Root POM: pom.xml
            Goal and options: clean install

        Click apply and save
    - Click the "Build Now"

### Step 6: Go back to Maven-Builder Job

    - Click the Workspace
        - Click the Webapp 
            - go "target folder"
                - You will see the build file example webapp.war


## Ansible Server Setup and  Ansible Installation

### Step 1: Launch a new Intances 

    Name: ansible-server
    AMI: Amazon Linux 2 AMIA
    keypair: Yes select your own

    Click Launch

### Step 2: Edit the Inbound Rules
    
    - Custom TCP
        - Port: 8080-8090
        - Any Rule
    - Save Rules

### Step 3: Access the Ansible Server

    - open the terminal and point the keypair to open the ssh


### Step 4: Install Ansible

    - Switch root
    ```
        sudo su
    ```
    - Rename the hostname

    ```
        hostnamectl set-hostname jenkins-server
    ```

    - add user for ansible

    ```
        useradd ansadmin
        passwd ansadmin
    ```

    - add in our sudoer

    ```
        visudo
    ```

    - find the the line "Same thing without a password

        - Add in the line
            ansadmin ALL=(ALL) NOPASSWD: ALL


    - Change the config of the ssh

        ```
            nano /etc/ssh/sshd_config
        ```
    - Find the line "PasswordAuthentication" change the no to yes

    - Restart the sshd deamon

        ```
            service sshd reload
        ```     

    - Switch to my new user "ansadmin"

        ```
            sudo su - ansadmin
        ```

    - Generate a new sshkeygen

    ```
    ssh-keygen
    pwd
    cd .ssh
    ls
    ```

    - Start the install the ansible

    ```
        sudo su
        amazon-linux-extras install ansible2
        ansible --version
    ```

## Integrate Ansible with Jenkins

Step 1: Setting jenkins for Ansible

    > Go to jenkins dashboard
        > Manage jenkins
            > System 
                > Go to Public over SSH
                    > SSH Server click add button
                        provide the info
                        - Name: Ansible-Server
                        - HOST : IP address
                        - USER: ansadmin
                    > Click Advance

                        - thick "Use password authentication or use a different key"
                        - provide the password

            > Click Apply,  "Test configuration" and SAVE

Step 2: Go the terminal to access the Ansible Server

    Make a folder from opt

    ```
    cd /opt

    sudo mkdir Docker
    ```

    Make permission for the folder

    ```
        sudo chown ansadmin:ansadmin Docker
        ll
    ```

Step 3: Create a new Item

    Click the the "New Item"
        Give the Name: Artifacts_on_ansible
        project: Maven project

    Click Ok


    Configuration

        - Source Code Management
            - Git
                - Provide the Repository URL:

        - Branch to build
            - Branch Specifer
                - */main

    Build
        Goals and options
            - type: clean install

    Post build Actions
        Add post-build action dropdown
            - Choose "Send build artifacts over SSH

            SSH Server
                - Server Name: ansible-server 
                - Transfer Set Source files
                    - "webapp/target/*.war
                - Remove prefix
                    - "webapp/target
                - Remote directory
                    - "//opt//Docker"

        Apply and Save

   Start Build by clicking

   Note: Check this if this will successfully


Step 4: Check the war files that have been build

    go to opt/Docker to check the build of artifacts of application war

    ```
    cd /opt/Docker
    date
    ll
    ```
 
 ## Install and Configure Docker on Ansible Server

 Step 1:  Go  to ansible server and install the docker

    ```
    sudo yum install docker
    id ansadmin
    sudo usermod -aG docker ansadmin
    id ansadmin
    sudo service docker start
    service docker status
    reboot
    sudo service docker start
    service docker status
    sudo su - ansadmin
    cd /opt/Docker
    nano Dockerfile
    ```

Step 2: Write the docker file 

    ```
    FROM tomcat:latest
    RUN cp -R /usr/local/tomcat/webapps.dist/* /usr/local/tomcat/webapps
    COPY ./*.war /usr/local/tomcat/webapps
    
    ```


## Create Ansible Playbook to Create Docker Image and Copy Image to DockerHub


Step 1: Modify the host of ansible

    Note: get the private IP address of the ansible
    ```
    ip add   
    sudo  nano /etc/ansible/hosts
    ```

Step 2: Copy the private IP address to hosts

```
[ansible]
172.x.x.x
```

```
ssh-copy-id 172.x.x.x
```

Step 3: Create the ansible playbook

```
nano regapp.yml
```


```
---
- hosts: ansible
  tasks:
  - name: Create docker image
    command: docker build -t regapp:latest .
    args:
      chdir: /opt/Docker
```

Run the playbook
```
ansible-playbook regapp.yml --check
ansible-playbook regapp.yml
```

Register the credential of docker from dockerhub

```
docker login
```


Modify the regapp.yml playbook and paste the following

```
---
- hosts: ansible
  tasks:
  - name: Create docker image
    command: docker build -t regapp:latest .
    args:
      chdir: /opt/Docker
  - name: Create tag to push image onto dockerhub
    command: docker tag regapp:latest mgelvoleo/reapp:latest

  - name: Push docker image
    command: docker push mgelvoleo/regapp:latest
```


Check the playbook and run againg

```
ansible-playbook regapp.yml --check

ansible-playbook regapp.yml 

docker images
```