import os
import requests
import re
import base64
from urllib3.exceptions import InsecureRequestWarning

class Fortigate:
    def __init__(self, admin_url, api_key, ssl_verify=True):

        self.admin_url = admin_url
        self.api_key = api_key
        self.ssl_verify = ssl_verify

        self.session = requests.session()
        self.session.headers.update({'Authorization': 'Bearer ' + self.api_key})
        
        if not self.ssl_verify:
            print("WARNING: SSL verification is disabled")
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def output_details(self):

        print("Admin URL is: " + self.admin_url)
        print("API Key: " + self.api_key)
        return True

    def backupConfig(self, encrypted=False, encryptionKey=None, backupDir=os.path.abspath(os.getcwd() + "/config_backups")):
        
        endpoint = "/api/v2/monitor/system/config/backup/"
        parameters = "?scope=global&destination=file"

        if not os.path.exists(backupDir):
            os.makedirs(backupDir)

        if encrypted:
            parameters = "{0}&password={1}&confirmPassword={1}".format(parameters, encryptionKey)

        response = self.session.get(self.admin_url + endpoint + parameters, verify=self.ssl_verify)

        if response.status_code == 200:
            filename = response.headers['content-disposition']
            filename = re.findall("filename=(.+)", filename)[0].replace('"','')

            with open(backupDir + "/" + filename, 'w') as configBackupWriter:
                configBackupWriter.write(response.text)
            
            print("Configuration Backup Successful")
            return True
        else:
            print("Configuration Backup Failed - {}".format(response.status_code))
            return False
    
    def uploadCertificate(self, name, certificate, key, password=None):

        endpoint = "/api/v2/monitor/vpn-certificate/local/import"
        payload = {
            'type': 'regular', 
            'scope': 'global', 
            'certname': name, 
            'file_content': certificate, 
            'key_file_content': key
        }

        if password:
            payload['password'] = password

        response = self.session.post(self.admin_url + endpoint, json=payload, verify=self.ssl_verify)
        
        if response.status_code == 200:
            print("Certificate Upload Successful - Certificate Name {}".format(name))
            return True
        else: 
            print("Certificate Upload Failed - {}".format(response.status_code))
            return False
    
    def setSSLVPNCertificate():
        pass
