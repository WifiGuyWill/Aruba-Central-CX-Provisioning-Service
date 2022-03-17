#!/usr/bin/python3
#(c) 2021 Will Smith - WILL@WIFI-GUYS.COM

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from flask import Flask, request, abort
from pycentral.base import ArubaCentralBase
import base64
import hashlib
import hmac

central_info = {
    "username": os.getenv('USERNAME'),
    "password": os.getenv('PASSWORD'),
    "client_id": os.getenv('CLIENT_ID'),
    "client_secret": os.getenv('CLIENT_SECRET'),
    "customer_id": os.getenv('CUSTOMER_ID'),
    "base_url": os.getenv('BASE_URL')
    }

token_id = os.getenv('WEBHOOK_TOKEN')
cx_ui_group = os.getenv('CX_UI_GROUP')

# Variables
ssl_verify = True
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)

app = Flask(__name__)
app.secret_key = 'S3cretK3y3'

# Validate message integrity
def verifyHeaderAuth(fullheaders, webhookData):
    # Token obtained from Aruba Central Webhooks page as provided in the input
    token = token_id.encode('utf-8')

    # Capture data - needs cleanup
    data = webhookData.decode('utf-8')
    service = fullheaders['X-Central-Service']
    delivery =fullheaders['X-Central-Delivery-Id']
    timestamp = fullheaders['X-Central-Delivery-Timestamp']
    header = service+delivery+timestamp
    hash = fullheaders['X-Central-Signature']

    # Construct HMAC digest message
    sign_data = str(data) + str(header)
    sign_data = sign_data.encode('utf-8')

    # Find Message signature using HMAC algorithm and SHA256 digest mod
    dig = hmac.new(token, msg=sign_data, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(dig).decode()
    if hash == signature:
        return True
    return False

@app.route('/webhook', methods=['POST'])
def webhook():
    
    #Validate HMAC that is a valid webhook from Aruba Central
    webhookData = request.get_data()
    fullheaders = request.headers
    verified = verifyHeaderAuth(fullheaders, webhookData)
    
    if verified != True:
        abort(401)
    
    # Incoming webhook data from Central
    if request.method == 'POST':
        data = request.get_json()
        # Process new CX Switch incoming webook - can add others in the future
        if (data['alert_type'] == 'New Switch Connected'):
            serial = (data['details']['serial'])
            print(serial)

            # Move CX Swtich into UI group
            apmove = central.command(apiMethod="POST", apiPath="/configuration/v1/devices/move", 
                apiData = {"group": cx_ui_group, "serials": [serial], "preserve_config_overrides": ["AOS_CX"]})
            print(apmove)
            return 'CX Switch Sucessfully Provisioned', 200

        else:
            return 'Webhook Not Yet Supported', 405

    else:
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
