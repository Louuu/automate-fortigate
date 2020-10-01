from fortigate_automation import Fortigate
from helper_functions import convertFileToBase64, generateUniqueCertName

sample60e = Fortigate("https://192.168.0.1:4443", "API_KEY", False)

certificate = convertFileToBase64("certificate.crt")
key = convertFileToBase64("key.key")
certificate_name = generateUniqueCertName()

sample60e.output_details()
sample60e.backupConfig()
sample60e.uploadCertificate(certificate_name, certificate, key)
