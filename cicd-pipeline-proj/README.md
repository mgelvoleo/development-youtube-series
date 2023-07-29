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



