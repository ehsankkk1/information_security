import requests

req = requests.get('https://127.0.0.1:5001',verify= 'teachers_certificates/rita_certificate.pem')
print(req.status_code)