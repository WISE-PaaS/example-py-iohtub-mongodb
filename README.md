# Example-python-Iothub-MongoDB


This is WIES-PaaS example-code include the mongodb and rabbitmq service。

**https://wise-paas.advantech.com/en-us**



## Quick Start

## Environment Prepare

cf-cli

[https://docs.cloudfoundry.org/cf-cli/install-go-cli.html](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html?source=post_page---------------------------)

python3

[https://www.python.org/downloads/](https://www.python.org/downloads/?source=post_page---------------------------)

![](https://cdn-images-1.medium.com/max/2000/1*iJwh3dROjmveF8x1rC6zag.png)



    git clone this respository
    
    #cf login -skip-ssl-validation -a {api.domain_name}  -u "account" -p "password"
    
    cf login –skip-ssl-validation -a api.wise-paas.io -u xxxxx@advtech.com.tw -p xxxxxx
    
    #check the cf status
    cf target


open the **`manifest.yml`** and editor the application name to yours，because the appication can't duplicate。
check the service instance name in **manifest.yml** and **WISE-PaaS**

![https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/MANI.PNG](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/MANI.PNG)

![https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/service_list_instance_name.PNG](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/service_list_instance_name.PNG)
 

open **`templates/index.html`**
    
    #change this **`python-demo-jimmy`** to your **application name**
    var ssoUrl = myUrl.replace('python-demo-jimmy', 'portal-sso');

(you need to check the service name in `index.py` and WISE-PaaS)
![https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/service-name.PNG](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/service-name.PNG)
![https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/code_image.PNG](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/code_image.PNG)

    #cf push {application name}
    cf push python-demo-mongodb
    
    #get the application environment
    cf env {application name} > env.json 
   

Edit the **publisher.py** `broker、port、username、password` you can find in env.json

* bokrer:"VCAP_SERVICES => p-rabbitmq => externalHosts"
* port :"VCAP_SERVICES => p-rabbitmq => mqtt => port"
* username :"VCAP_SERVICES => p-rabbitmq => mqtt => username"
* password: "VCAP_SERVICES => p-rabbitmq => mqtt => password"

open two terminal
    
    #cf logs {application name}
    cf logs python-demo-mongodb

.

    python publisher.py

![https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/ALREADY.PNG](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/ALREADY.PNG)

![https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/TEMP.PNG](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/TEMP.PNG)

# Step By Step Tutorial

[https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/README.md](https://github.com/WISE-PaaS/example-python-iohtub-mongodb/blob/master/source/README.md)
