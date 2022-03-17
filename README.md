# Service to Auto Provision CX Switches in Aruba Central


![ACCPS](https://github.com/WifiGuyWill/Aruba-Central-CX-Provisioning-Service/blob/main/img/ACCPS.jpg?raw=true "ACCPS")

This service helps to auotmate the provision process for CX switches in Aruba Central.


# How It Works:

*Verify CX switches are added to Central device inventory and subscription is applied
*Assign CX switches to the pre-provisioning template group
*Switch contacts Aruba Central and get the initial config
*Webhook is sent to the CX provisioning service
*Provisioning service sends API POST message to move the CX switch into the UI group
*Switch is moved into the UI group and retains the initial config from the template
*Switch is now fully configured and can be updated/modified using UI or MultiEdit


# First Steps:

  1. Log into Aruba Central from the Account Home page:  
     * API Gateway > System Apps & Tokens > Create a new key
     * Webhooks > Click the + sign > Enter the URL where the CX provisioning service will be posted "https://your-server.com/webhook"
     * Hit save and note the Token
  2. Launch the Network Dashboard:  
     * Global > Alerts & Events > Config  
     * Under Access Point > Enable AP Detect > Select the Webhook for the CX switch provisioning service
 
# Install Instructions:

  1. Copy the files to host
  2. Open dockerfile and add the Aruba Central Credentials, Webhook Token, and Central Group new CX switches should be placed into.

    > ENV USERNAME=xxxxxxxxxx@email.com  
    > ENV PASSWORD=xxxxxxxxxx  
    > ENV CLIENT_ID=xxxxxxxxxx  
    > ENV CLIENT_SECRET=xxxxxxxxxx  
    > ENV CUSTOMER_ID=xxxxxxxxxx  
    > ENV BASE_URL=https://apigw-prod2.central.arubanetworks.com   
    > ENV WEBHOOK_TOKEN=xxxxxxxxxx  
    > ENV CX_UI_GROUP=xxxxxxxxxx
  
  3. Create the container "docker build -t accps:latest ."
  4. Start the container "docker run -p 5000:5000 accps"
  
- - - -

This container includes gunicorn web-server, modify the wsgi config as needed.


Question - Feel free to contact me:   
#(c) 2022 Will Smith - WILL@WIFI-GUYS.COM
