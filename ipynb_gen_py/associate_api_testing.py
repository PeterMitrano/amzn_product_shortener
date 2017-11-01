
# coding: utf-8

# In[20]:

import base64
import datetime
import hashlib
import hmac 
import requests
import configparser
import urllib.parse
from collections import OrderedDict


def sign(key, msg):
    return base64.b64encode(hmac.new(key.encode("utf-8"), msg.encode('utf-8'), hashlib.sha256).digest())

# Read AWS access key from env. variables or configuration file. Best practice is NOT
# to embed credentials in code.
parser = configparser.ConfigParser()
parser.read('secrets.ini')
associate_id = parser['default']['associate_id']
access_key = parser['default']['access_key']
secret_key = parser['default']['secret_key']

method = 'GET'
region = 'us-east-1'
endpoint = "webservices.amazon.com"
request_uri = "/onca/xml"

params = OrderedDict([
  ("AWSAccessKeyId", access_key),
  ("AssociateTag", associate_id),
  ("Keywords", "book"),
  ("Operation", "ItemSearch"),
  ("SearchIndex", "All"),
  ("Service", "AWSECommerceService"),
])

# Set current timestamp if not set
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y-%m-%dT%H:%M:%S.000Z')
datestamp = t.strftime('%Y%m%d')
params["Timestamp"] = amzdate

# Generate the canonical query
params_list = []
for key, value in params.items():
    params_list.append(urllib.parse.quote_plus(key) + "=" + urllib.parse.quote_plus(value))
canonical_query_string = "&".join(params_list)

# Generate the string to be signed
string_to_sign = "GET" + "\n" + endpoint + "\n" + request_uri + "\n" + canonical_query_string

signature = sign(secret_key, string_to_sign)

request_url = "http://" + endpoint + request_uri + "?" + canonical_query_string + "&" + "Signature=" + urllib.parse.quote_plus(signature)


# In[21]:

response = requests.get(request_url)


# In[23]:

import xml.etree.ElementTree as ET
from IPython.core.display import display, HTML


print(response.ok)
try:
    tree = ET.fromstring(response.content)
    print(tree)
except ET.ParseError:
    display(HTML(str(response.content)))


# In[ ]:



