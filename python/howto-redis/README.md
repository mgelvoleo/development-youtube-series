# How to make redis as database to our python apps

## Step 1: run and deploy 3 redis
```
docker network create redis
```


#redis-0
```
docker run -d --rm --name redis-0 `
    --net redis `
    -v ${PWD}/redis-0:/etc/redis/ `
    redis:6.0-alpine redis-server /etc/redis/redis.conf
```


#redis-1
```
docker run -d --rm --name redis-1 `
    --net redis `
    -v ${PWD}/redis-1:/etc/redis/ `
    redis:6.0-alpine redis-server /etc/redis/redis.conf
```

#redis-2
```
docker run -d --rm --name redis-2 `
    --net redis `
    -v ${PWD}/redis-2:/etc/redis/ `
    redis:6.0-alpine redis-server /etc/redis/redis.conf
```

# Step 3: Start the sentinel mode
```
docker run -d --rm --name sentinel-0 --net redis `
    -v ${PWD}/sentinel-0:/etc/redis/ `
    redis:6.0-alpine `
    redis-sentinel /etc/redis/sentinel.conf
```

```
docker run -d --rm --name sentinel-1 --net redis `
    -v ${PWD}/sentinel-1:/etc/redis/ `
    redis:6.0-alpine `
    redis-sentinel /etc/redis/sentinel.conf
```

```
docker run -d --rm --name sentinel-2 --net redis `
    -v ${PWD}/sentinel-2:/etc/redis/ `
    redis:6.0-alpine `
    redis-sentinel /etc/redis/sentinel.conf
```


# Step 4:  Make a dev environment of python using docker

* dockerfile

```
FROM python:3.9.6-alpine3.13 as dev
WORK /work

```

 ## Step 4.1
   * type the following docker command 
   ```
    docker build --target dev . -t python
    docker run -it -v ${PWD}:/work -p 5000:5000 --net redis python sh
   ```

## Step 5: Create src\ folder and inside create python file

# Step 5.1: Create src\app.py

# Step 5.2: Paste the following import module

# Step 5.3: And also set a global variable for the location of our videos json file:

```
import os.path
import csv
import json
from flask import Flask
from flask import request

dataPath = "./customers.json"

class Customer:
  def __init__(self, c="",f="",l=""):
    self.customerID = c
    self.firstName  = f
    self.lastName   = l
  def fullName(self):
    return self.firstName + " " + self.lastName

def getCustomers():
  if os.path.isfile(dataPath):
    with open(dataPath, newline='') as customerFile:
      data = customerFile.read()
      customers = json.loads(data)
      return customers
  else: 
    return {}   

def getCustomer(customerID):
  customers = getCustomers()

  if customerID in customers:
    return customers[customerID]
  else:
    return {}

def updateCustomers(customers):
  with open(dataPath, 'w', newline='') as customerFile:
    customerJSON = json.dumps(customers)
    customerFile.write(customerJSON)
```



## Step 6: Create a file json inside of src/ and name id "customer.json" for editor and command "mkdir src/customer.json

```
mkdir src/customer.json
```

## Step 7: Paste the sample record customer.json
```
{
  "a": {
    "customerID": "a",
    "firstName": "James",
    "lastName": "Baker"
  },
  "b": {
    "customerID": "b",
    "firstName": "Jonathan",
    "lastName": "D"
  },
  "c": {
    "customerID": "c",
    "firstName": "Aleem",
    "lastName": "Janmohamed"
  },
  "d": {
    "customerID": "d",
    "firstName": "Ivo",
    "lastName": "Galic"
  },
  "e": {
    "customerID": "e",
    "firstName": "Joel",
    "lastName": "Griffiths"
  },
  "f": {
    "customerID": "f",
    "firstName": "Michael",
    "lastName": "Spinks"
  },
  "g": {
    "customerID": "g",
    "firstName": "Victor",
    "lastName": "Savkov"
  }
}



```