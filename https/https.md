# Nginx - HTTPS

[Back](../README.md)

- [Nginx - HTTPS](#nginx---https)
  - [Self-host using OpenSSL](#self-host-using-openssl)
  - [Certificate Authority - Let's Encrypt](#certificate-authority---lets-encrypt)

---

## Self-host using OpenSSL

```sh
# Create a directory for SSL certificates
sudo mkdir -p /etc/nginx/ssl
cd /etc/nginx/ssl

# Generate the private key and certificates
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx-selfsigned.key \
    -out /etc/nginx/ssl/nginx-selfsigned.crt

# # generate private key
# openssl genrsa -out private.key 2048

# # generate Certificate Signing Request(CSR)
# openssl req -new -key private.key -out cert.csr

# # generate pem
# openssl x509 -req -in cert.csr -out cacert.pem -signkey private.key

# confirm
ls -l /etc/nginx/ssl
# -rw-r--r-- 1 root root 1424 Jun 27 10:31 nginx-selfsigned.crt
# -rw------- 1 root root 1704 Jun 27 10:30 nginx-selfsigned.key
```

- Configure Nginx

```conf
server {
    listen 80;
    server_name 192.168.100.105;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name 192.168.100.105;

    # certificate
    ssl_certificate             /etc/nginx/ssl/nginx-selfsigned.crt;
    # private key
    ssl_certificate_key         /etc/nginx/ssl/nginx-selfsigned.key;
    # ssl valid session
    ssl_session_timeout         5m;
    # Basic SSL settings
    ssl_protocols               TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers   on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;

    root /var/www/localhost;
    index index.html;
    error_page 404 /404.html;

    location / {
      add_header X-debug-uri "$uri";
      try_files $uri $uri/ =404;
    }
}
```

- Reload

```sh
# Set Proper Permissions
sudo chmod 600 /etc/nginx/ssl/nginx-selfsigned.key
sudo chmod 644 /etc/nginx/ssl/nginx-selfsigned.crt

sudo nginx -t && sudo nginx -s reload

curl -k https://192.168.100.105
# <!doctype html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <title>Hello, Nginx!</title>
#     <link rel="stylesheet" href="style.css">
# </head>
# <body>
#     <h1>Hello, Nginx!</h1>
#     <p>We have just configured our Nginx web server on Ubuntu Server!</p>
# </body>
# </html>


```

## Certificate Authority - Let's Encrypt
