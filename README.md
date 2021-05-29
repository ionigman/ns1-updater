# ns1-updater
python3 dynamic DNS updater for NS1's managed DNS service

You'll need to use the `requests` library. NS1 API key with manage_zones permissions is also required. 

This script will check the public IP of the machine where it is running against the A record for the domain you specify every ten seconds. 
If they do not match, the A record will be updated to match the public IP. 

This is provided without any warranty of any sort. Use at your own risk. 
