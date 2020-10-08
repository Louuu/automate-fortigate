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

    def outputDetails(self):

        print("Admin URL is: " + self.admin_url)
        print("API Key: " + self.api_key)
        return True

    def backupConfig(self, encrypted=False, encryptionKey=None):

        endpoint = "/api/v2/monitor/system/config/backup/"
        parameters = {
            'scope': 'global',
            'destination': 'file'
        }

        if encrypted:
            parameters['password'] = encryptionKey
            parameters['confirmPassword'] = encryptionKey

        response = self.session.get(self.admin_url + endpoint, params=parameters, verify=self.ssl_verify)

        if response.status_code == 200:

            filename = response.headers['content-disposition']
            filename = re.findall("filename=(.+)", filename)[0].replace('"', '')

            output = {
                'configuration': response.text,
                'original_filename': filename
            }

            print("Configuration backup successful")
            return output
        else:
            print("Configuration backup failed")
            return False

    def uploadLocalCertificate(self, certificate_name, certificate, key, password=None):

        endpoint = "/api/v2/monitor/vpn-certificate/local/import"
        payload = {
            'type': 'regular',
            'scope': 'global',
            'certname': certificate_name,
            'file_content': certificate,
            'key_file_content': key
        }

        if password:
            payload['password'] = password

        response = self.session.post(self.admin_url + endpoint, json=payload, verify=self.ssl_verify)

        if response.status_code == 200:
            print("Certificate upload successful - certificate came {}".format(certificate_name))
            return True
        else:
            print("Certificate upload failed - {}".format(response.status_code))
            return False

    def setSSLVPNCertificate(self, certificate_name):

        endpoint = "/api/v2/cmdb/vpn.ssl/settings"
        payload = {
            'servercert': certificate_name
        }

        response = self.session.put(self.admin_url + endpoint, json=payload, verify=self.ssl_verify)

        if response.status_code == 200:
            print("SSL VPN certificate configured successfully")
            return True
        else:
            print("SSL VPN certificate configuration failed")
            return False

    def setInspectionProfileServerCertificate(self, profile_name, certificate_name):

        endpoint = "/api/v2/cmdb/firewall/ssl-ssh-profile/{0}".format(profile_name)
        payload = {
            'servercert': certificate_name
        }

        response = self.session.put(self.admin_url + endpoint, json=payload, verify=self.ssl_verify)

        if response.status_code == 200:
            print("Inspection profile certificate configured successfully for {0}".format(profile_name))
            return True
        else:
            print("Inspection profile certificate configuration failed for {0}".format(profile_name))
