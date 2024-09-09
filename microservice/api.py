import urlparse,urllib,urllib2,requests,cookielib
import base64
import json,gzip,zlib,sys,csv
import time
import StringIO
import os
import ssl
import socket

headers = {"Accept":"application/json","Content-type":"application/x-www-form-urlencoded; charset=UTF-8","User_Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
key_file = os.environ['LAV_DIR'] + '/credenza/hosts.json'
cred = []
with open(key_file) as f:
    cred = json.load(f)['api']['tdg']

baseUrl = cred['url'] + ":" + cred['port']
sock = socket.socket()
sock.connect((cred['url'][8:],int(cred['port'])))
sock = ssl.wrap_socket(sock,  cert_reqs=ssl.CERT_REQUIRED,  ca_certs="cacerts.txt")

print("wget " + baseUrl + " --ca-certificate=mycertfile.pem")

# security hole here - there should be an error about mismatched host name
# manual check of hostname
cert = sock.getpeercert()
for field in cert['subject']:
  if field[0][0] == 'commonName':
    certhost = field[0][1]
    if certhost != HOST:
      raise ssl.SSLError("Host name '%s' doesn't match certificate host '%s'"
                         % (HOST, certhost))


headers = {"Authorization":"Basic "+base64.standard_b64encode(cred['user']+":"+cred['pass']),"Content-Type":"application/x-www-form-urlencoded"}
sData={}
resq = requests.get(baseUrl+'/v1/locations/101',headers=headers)

print("openssl s_client -showcerts -connect " + baseUrl + ' </dev/null 2>/dev/null|openssl x509 -outform PEM > ' + os.environ['LAV_DIR'] + '/credenza/ml_cert.pem')

print(ssl.get_server_certificate(baseUrl, ssl_version=ssl.PROTOCOL_TLSv1, ca_certs=None))

print("curl –user cred['user']:cred['password'] –cert ./training.crt –key ./training-key.pem -X GET 'https://motionlogic.de/api-telia-se/v1/locations/100’ -k")
print("wget https:/server.edu:443/somepage --ca-certificate=mycertfile.pem")


import socket
import ssl

HOST = "www.example.com"
PORT = 443
HOST = socket.getaddrinfo(HOST, PORT)[0][4][0]
print(HOST)
sock = socket.socket()
sock.connect((HOST, PORT))

# wrap socket to add SSL support
sock = ssl.wrap_socket(sock,
  # flag that certificate from the other side of connection is required
  # and should be validated when wrapping 
  cert_reqs=ssl.CERT_REQUIRED,
  # file with root certificates
  ca_certs="cacerts.txt"
)

# security hole here - there should be an error about mismatched host name
# manual check of hostname
cert = sock.getpeercert()
for field in cert['subject']:
  if field[0][0] == 'commonName':
    certhost = field[0][1]
    if certhost != HOST:
      raise ssl.SSLError("Host name '%s' doesn't match certificate host '%s'"
                         % (HOST, certhost))



from requests import Request, Session
s = Session()
req = Request('POST',baseUrl)
prepped = s.prepare_request(req)
resp = s.send(prepped, verify=False, cert="/tmp/cert.pem")


auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password(realm='PDQ Application',
                          uri='https://mahler:8092/site-updates.py',
                          user='klem',
                          passwd='kadidd!ehopper')
opener = urllib2.build_opener(auth_handler)
# ...and install it globally so it can be used with urlopen.
urllib2.install_opener(opener)
urllib2.urlopen('http://www.example.com/login.html')

handle = urllib2.Request(url)
authheader =  "Basic %s" % base64.encodestring('%s:%s' % (username, password))
handle.add_header("Authorization", authheader)
