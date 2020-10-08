import os
from fortigate_automation import Fortigate
from helper_functions import convertFileToBase64, generateUniqueCertName

backupDir = os.path.abspath(os.getcwd() + "/config_backups")
sample60e = Fortigate("https://192.168.0.1:4443", "API_KEY", False)

certificate = convertFileToBase64("certificate.crt")
key = convertFileToBase64("key.key")
certificate_name = generateUniqueCertName()

sample60e.outputDetails()
backup = sample60e.backupConfig()
sample60e.uploadLocalCertificate(certificate_name, certificate, key)
sample60e.setSSLVPNCertificate(certificate_name)
sample60e.setInspectionProfileServerCertificate("endpoint-certificate", certificate_name)

if not os.path.exists(backupDir):
    os.makedirs(backupDir)

with open(backupDir + "/" + backup['original_filename'], 'w') as configBackupWriter:
    configBackupWriter.write(backup['configuration'])
