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

## Step 7: Update the app.py start instantiate flask and endpoint


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




app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_customers():
    customers = getCustomers()
    return json.dumps(customers)


@app.route("/get/<string:customerID>", methods=['GET'])
def get_customer(customerID):
    customer = getCustomer(customerID)

    if customer == {}:
      return {}, 404
    else:
      return customer

@app.route("/set", methods=['POST'])
def add_customer():
    jsonData = request.json

    if "customerID" not in jsonData:
      return "customerID required", 400
    if "firstName" not in jsonData:
      return "firstName required", 400
    if "lastName" not in jsonData:
      return "lastName required", 400
    
    customers = getCustomers()
    customers[jsonData["customerID"]] = Customer( jsonData["customerID"], jsonData["firstName"], jsonData["lastName"]).__dict__
    updateCustomers(customers)
    return "success", 200


```



## Step 8: Create a requirement files that will install version of flask
```
.
./
./redis/requiments.txt
```

## Step 8.1: Paste the version of FLASK
```
FLASK == 2.0.2

```

## Step 9: Install by using the command
```
pip install -r requirements.txt
```

## Step 8: Expose inside the bash of docker

```
export FLASK_APP=src/app
flask run -h 0.0.0 -p 5000
```

## Step 9: Access in your browser localhost:5000

## Step 10: add in the requirement.txt for install the the redis
```
FLASK == 2.0.2
redis == 3.5.3
```

## Step 11: Instal redis by using the command
```
pip install -r requirements.txt
```


## Step 12: Test first the redis sentinel inside container

```
python 
```

```
from redis.sentinel import Sentinel
```

```
sentinel = Sentinel([('sentinel-0', 5000),('sentinel-1', 5000),('sentinel-2', 5000)], socket_timeout=0.1)
sentinel.discover_master('mymaster')
sentinel.discover_slaves('mymaster')

master = sentinel.master_for('mymaster',password = "a-very-complex-password-here", socket_timeout=0.1)

slave = sentinel.slave_for('mymaster',password = "a-very-complex-password-here", socket_timeout=0.1)

master.set('foo', 'bar')
slave.get('foo')
```

## Step 13: Test to remove the master sentinel if what is happen
```
# stop current master
docker rm -f redis-0
```

```
* Make a new master because remove the one
master.set('foo', 'bar2')
slave.get('foo')
sentinel.discover_master('mymaster')
sentinel.discover_slaves('mymaster')
```

* To recover from failure
```
docker run -d --rm --name redis-0 `
    --net redis `
    -v ${PWD}/redis-0:/etc/redis/ `
    redis:6.0-alpine redis-server /etc/redis/redis.conf

sentinel.discover_slaves('mymaster')
```

## Step 13: Its time to connect the apps to redis, and update the code

```
import os.path
import csv
import json
from flask import Flask
from flask import request
import os

dataPath = "./customers.json"


redis_sentinels = os.environ.get('REDIS_SENTINELS')
redis_master_name = os.environ.get('REDIS_MASTER_NAME')
redis_password = os.environ.get('REDIS_PASSWORD')


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




app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_customers():
    customers = getCustomers()
    return json.dumps(customers)


@app.route("/get/<string:customerID>", methods=['GET'])
def get_customer(customerID):
    customer = getCustomer(customerID)

    if customer == {}:
      return {}, 404
    else:
      return customer

@app.route("/set", methods=['POST'])
def add_customer():
    jsonData = request.json

    if "customerID" not in jsonData:
      return "customerID required", 400
    if "firstName" not in jsonData:
      return "firstName required", 400
    if "lastName" not in jsonData:
      return "lastName required", 400
    
    customers = getCustomers()
    customers[jsonData["customerID"]] = Customer( jsonData["customerID"], jsonData["firstName"], jsonData["lastName"]).__dict__
    updateCustomers(customers)
    return "success", 200


```

* After add the line of code exit in the container, to go back root and run docker by the following command,We will need to restart our container so we can inject these environment variables.

```
docker run -it -p 5000:5000 `
  --net redis `
  -v ${PWD}:/work `
  -e REDIS_SENTINELS="sentinel-0:5000,sentinel-1:5000,sentinel-2:5000" `
  -e REDIS_MASTER_NAME="mymaster" `
  -e REDIS_PASSWORD="a-very-complex-password-here" `
  python sh

```

# Inside the container shell 

```
pip install -r requirements.txt
```


# Step 14: Update by add a line "from redis.sentinel import Sentinel"

```
import os.path
import csv
import json
from flask import Flask
from flask import request
import os
from redis.sentinel import Sentinel



dataPath = "./customers.json"


redis_sentinels = os.environ.get('REDIS_SENTINELS')
redis_master_name = os.environ.get('REDIS_MASTER_NAME')
redis_password = os.environ.get('REDIS_PASSWORD')


def redis_command(command, *args):
  max_retries = 3
  count = 0
  backoffSeconds = 5
  while True:
    try:
      return command(*args)
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
      count += 1
      if count > max_retries:
        raise
    print('Retrying in {} seconds'.format(backoffSeconds))
    time.sleep(backoffSeconds)


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




app = Flask(__name__)

sentinels = []

for s in redis_sentinels.split(","):
  sentinels.append((s.split(":")[0], s.split(":")[1]))

redis_sentinel = Sentinel(sentinels, socket_timeout=5)
redis_master = redis_sentinel.master_for(redis_master_name,password = redis_password, socket_timeout=5)



@app.route("/", methods=['GET'])
def get_customers():
    customers = getCustomers()
    return json.dumps(customers)


@app.route("/get/<string:customerID>", methods=['GET'])
def get_customer(customerID):
    customer = getCustomer(customerID)

    if customer == {}:
      return {}, 404
    else:
      return customer

@app.route("/set", methods=['POST'])
def add_customer():
    jsonData = request.json

    if "customerID" not in jsonData:
      return "customerID required", 400
    if "firstName" not in jsonData:
      return "firstName required", 400
    if "lastName" not in jsonData:
      return "lastName required", 400
    
    customers = getCustomers()
    customers[jsonData["customerID"]] = Customer( jsonData["customerID"], jsonData["firstName"], jsonData["lastName"]).__dict__
    updateCustomers(customers)
    return "success", 200


```