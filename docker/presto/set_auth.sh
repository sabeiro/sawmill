#keytool -import -keystore <JAVA_HOME>/jre/lib/security/cacerts -trustcacerts -alias ldap_server -file ldap_server.crt
#htpasswd -B -C 10 password.db api_ingest
#hostname --fqdn
#keytool -genkeypair -alias coordinator -keyalg RSA -keystore presto_keystore.jks

openssl req -x509 -newkey rsa:1024 -keyout privateKey.pem -out certificateChain.pem -days 365 -nodes -subj '/C=US/ST=Washington/L=Seattle/O=MyOrg/OU=MyDept/CN=*.us-west-2.compute.internal'
cp certificateChain.pem trustedCertificates.pem
zip -r -X my-certs.zip certificateChain.pem privateKey.pem trustedCertificates.pem

# cert for localhost
openssl genrsa -des3 -out rootCA.key 2048
