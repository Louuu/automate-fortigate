import base64
from uuid import uuid4


def convertStringToBase64(string):

    string_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(string_bytes)
    string_base64 = base64_bytes.decode('ascii')
    return string_base64


def convertFileToBase64(filename):
    with open(filename, 'r') as certificateFile:
        file_base64 = convertStringToBase64(certificateFile.read())
    return file_base64


def generateUniqueCertName():
    unique_certificate_name = uuid4().hex
    return unique_certificate_name
