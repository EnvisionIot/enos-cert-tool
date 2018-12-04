# EnOS Certificate Generating Tool
This repo contains the Python script that helps you get the EnOS CA root certificate, generate the local private key, and apply the X.509 cerficate issued by EnOS.

* [Install Dependencies](#python)
* [Configure Certificate Generation Properties](#configuration)
* [Run Python Script to Generate Certificates](#run)
* [What to do Next](#next)

<a name="python"></a>
## Install Dependencies
To use the Python script, you will need Python 2.7.10+, and `pip` is required.

This tool depends on `enos-api-sdk-python`, you can use pip to install the dependency with the following command:

```bash
pip install enos-api-sdk-python
```

<a name="configuration"></a>
## Configure Certificate Generation Properties

To generate the X.509 certificates, you need to first configure the `get_cert.ini` file that defines the properties to use for certificate generation. The properties are described as follows:

```ini
[required]
root_cert_url            # the EnOS CA Root URL
CN                       # the common name in the certificate, recommend to fill with the asset_id of the gateway device
org_id                   # the OU ID
product_key              # the gateway product key
device_key               # the gateway device key
api_url                  # the EnOS API URL
access_key               # the access key of the application created in EnOS
secret_key               # the secret key of the application created in EnOS

[option]
LOCATION                 # the location for the OU in the certficate
OU                       # the OU name in the certificate
password                 # the password for the private key
```

<a name="run"></a>
## Run Python Script to Generate Certificates
After you complete configuring the properties in the `get_cert.ini` file, run the following command to generate the certficate files：
```bash
python get_cert.py
```

You will find the following files generated in the directory:
```bash
edge_ca.pem     # the CA root file of EnOS
edge.key        # the private key of the local device
edge.pem        # the certificate for the local device issued by EnOS
```
<a name="next"></a>
## What to do Next

Place the generated certificate files into your edge project for establishing secure MQTT connection to EnOS IoT Hub.
