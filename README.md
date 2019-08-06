# Example-python-Iothub-MongoDB

This is WIES-PaaS example-code include the mongodb and rabbitmq service。

[cf-introduce](https://advantech.wistia.com/medias/ll0ov3ce9e)

[IotHub](https://advantech.wistia.com/medias/up3q2vxvn3)

### Quick Start

## Environment Prepare

cf-cli

[https://docs.cloudfoundry.org/cf-cli/install-go-cli.html](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html?source=post_page---------------------------)

python3

[https://www.python.org/downloads/](https://www.python.org/downloads/?source=post_page---------------------------)

![](https://cdn-images-1.medium.com/max/2000/1*iJwh3dROjmveF8x1rC6zag.png)

python3 package(those library you can try application in local):

    #mqtt
    pip3 install paho-mqtt
    #python-backend
    pip3 install Flask
    #python mongodb library
    pip3 install flask_pymongo

## Download this file

    git clone this respository

![Imgur](https://i.imgur.com/JNJmxFy.png)

    #cf login -a api.{domain name} -u {WISE-PaaS/EnSaaS account} -p {WISE-PaaS/EnSaaS password}
    cf login -a api.wise-paas.io -u xxxxx@advantech.com -p xxxxxxxx

    #check the cf status
    cf target

## Application Introduce

#### index.py

This is a simple backend application use flask，you can run it use `python3 index.py` and listen on [localhost:3000](localhost:3000)，and the port can get the `3000` or port on WISE-PaaS。

```py

from flask import Flask, render_template
import json
import paho.mqtt.client as mqtt
import os

# mongodb need
from flask_pymongo import PyMongo
from flask import jsonify, request, abort
import datetime
app = Flask(__name__)

# port from cloud environment variable or localhost:3000
port = int(os.getenv("PORT", 3000))


@app.route('/', methods=['GET'])
def root():

    if(port == 3000):
        return 'hello world! i am in the local'
    elif(port == int(os.getenv("PORT"))):
        return render_template('index.html')


if __name__ == '__main__':
        # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)

```

`vcap_services` can get the application config on WISE-PaaS，it can help get the credential of your (iothub)mqtt service instance，`client=mqtt.connect` can help us connect to mqtt and when we connect we will subscribe the `/hello` topic in `on_connect`，`on_message` can receivec and we save it to the database。

we use `pyMongo` to control our MongoDB database `app.config` is the mongodb uri in WISE-PaaS we bind，and we create a collection name `temp`。

**Notice(you need to check the service name in `index.py` and WISE-PaaS)**

![Imgur](https://i.imgur.com/6777rmg.png)

```py
IOTHUB_SERVICE_NAME = 'p-rabbitmq'
DB_SERVICE_NAME = 'mongodb-innoworks'

# application environment
vcap_services = os.getenv('VCAP_SERVICES')
vcap_services_js = json.loads(vcap_services)

# mqtt
credentials = vcap_services_js[IOTHUB_SERVICE_NAME][0]['credentials']['protocols']
mqtt_credential = credentials['mqtt']
broker = mqtt_credential['host']
username = mqtt_credential['username'].strip()
password = mqtt_credential['password'].strip()
mqtt_port = mqtt_credential['port']

# mongodb
uri = vcap_services_js[DB_SERVICE_NAME][0]['credentials']['uri']
app.config['MONGO_URI'] = uri
mongo = PyMongo(app)
collection = mongo.db.temp

# mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # subscribe the /helo this topic
    client.subscribe("/hello")
    print('subscribe on /hello')


def on_message(client, userdata, msg):
    print(msg.topic+','+msg.payload.decode())
    ti =  datetime.datetime.now()
    topic = msg.topic
    data = msg.payload.decode()
    temp_id = collection.insert({'date': ti, 'topic': topic, 'data': data})
    new_temp = collection.find_one({'_id': temp_id})
    output = {'date': new_temp['date'],
              'topic': new_temp['topic'], 'data': new_temp['data']}

    print(output)


client = mqtt.Client()

client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, mqtt_port, 60)
client.loop_start()

```

This is the api can help us debug，`/temp`(get) can give all data we save in mongodb，and `/insert`(post) can send fake data to the database。

```py

@app.route('/temp', methods=['GET'])
def get_all_temps():

    output = []
    for s in collection.find():

        output.append(
            {'date': s['date'], 'topic': s['topic'], 'data': s['data']})
    return jsonify({'rsult': output})


@app.route('/insert', methods=['POST'])
def insert_data():

    if not request.json:
        abort(400)
    ti = datetime.datetime.now()
    topic = request.json['topic']
    data = request.json['data']
    temp_id = collection.insert({'date': ti, 'topic': topic, 'data': data})
    new_temp = collection.find_one({'_id': temp_id})
    output = {'date': new_temp['date'],
              'topic': new_temp['topic'], 'data': new_temp['data']}

    return jsonify({'retult': output})

```

open the **`manifest.yml`** and editor the application name to yours，because the appication can't duplicate。
check the service instance name in **manifest.yml** and **WISE-PaaS**

![Imgur](https://i.imgur.com/2A2HDzz.png)

![Imgur](https://i.imgur.com/VVMcYO8.png)

## SSO(Single Sign On)

This is the [sso](https://advantech.wistia.com/medias/vay5uug5q6) applicaition，open **`templates/index.html`** and editor the `ssoUrl` to your application name，

If you don't want it，you can ignore it。

```
#change this **`python-demo-jimmy`** to your **application name**
var ssoUrl = myUrl.replace('python-demo-jimmy', 'portal-sso');
```

## Push application to the WISE-PaaS

    #cf push {application name}
    cf push python-demo-mongodb

    #get the application environment
    cf env {application name} > env.json

![Imgur](https://i.imgur.com/ZjrjuTW.png)

Edit the **publisher.py** `broker、port、username、password` you can find in env.json

- bokrer:"VCAP_SERVICES => p-rabbitmq => externalHosts"
- port :"VCAP_SERVICES => p-rabbitmq => mqtt => port"
- username :"VCAP_SERVICES => p-rabbitmq => mqtt => username"
- password: "VCAP_SERVICES => p-rabbitmq => mqtt => password"

open two terminal

#cf logs {application name}
cf logs python-demo-mongodb

.

    python publisher.py

![https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/ALREADY.PNG](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/ALREADY.PNG)

![https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/TEMP.PNG](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/TEMP.PNG)

# Step By Step Tutorial

[https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/README.md](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/README.md)
