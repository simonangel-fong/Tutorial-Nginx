# Nginx - Common Command

[Back](../README.md)

---

## Configure File

- Nginx configuration file:
  - `/etc/nginx/nginx.conf`
  - `/usr/local/nginx/conf/nginx.conf `
  - `/usr/local/etc/nginx/nginx.conf `

---

## Common Commands

- Service

| CMD                       | DESC                                        |
| ------------------------- | ------------------------------------------- |
| `systemctl status nginx`  | View Nginx status                           |
| `systemctl start nginx`   | Start Nginx                                 |
| `systemctl stop nginx`    | Stop Nginx                                  |
| `systemctl restart nginx` | Restart Nginx                               |
| `systemctl reload nginx`  | Reload Nginx (without dropping connections) |
| `systemctl enable nginx`  | Enable Nginx to start on boot               |
| `systemctl disable nginx` | Disable automatic start of Nginx on boot    |

- Nginx Process

| CMD                    | DESC                             |
| ---------------------- | -------------------------------- |
| `nginx -t`             | Check Nginx configuration syntax |
| `nginx -v`             | Check Nginx version              |
| `nginx -s stop`        | Fast shutdown                    |
| `nginx -s quit`        | Graceful shutdown                |
| `nginx -s reload`      | Reload the cf                    |
| `nginx -s reopen`      | Reopen the log file              |
| `ps -ax \| grep nginx` | Reopen the log file              |

- Log

| CMD                         | Desc                     |
| --------------------------- | ------------------------ |
| `/var/log/nginx/access.log` | Access Nginx access logs |
| `/var/log/nginx/error.log`  | Access Nginx error logs  |

- Test if Nginx is running and listening on ports:
  - `sudo netstat -tuln | grep nginx`

---

## Configuration File

- Directives and Syntax

  - **Directives**:
    - These are keywords that define parameters for Nginx behavior (e.g., `server_name`, `location`, `root`).
  - **Syntax**:
    - Nginx configuration follows a strict syntax with blocks enclosed in curly braces `{}` and directives ending with a semicolon `;`.

- Includes and Modularization
  - Nginx supports modularization through the use of **include files** (`include /path/to/file`) and snippets, allowing configuration to be split across multiple files for easier management and organization.

---

- Reload and Testing
  - test the syntax validity: `sudo nginx -t`
  - apply changes without dropping active connections: `sudo systemctl reload nginx`

---

- Default CF

```conf
# Global Block
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /run/nginx.pid;

# Events Block
events {
    worker_connections  1024;
}

# HTTP Block: configuration directives related to HTTP traffic
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

---

### Global Block

- settings that apply to the whole Nginx server.

```conf
user nginx; # user that Nginx will run as
worker_processes auto; # how many worker processes Nginx should spawn to handle requests.
```

---

### Events Block:

- settings related to events and connections.

```conf
events {
    worker_connections 1024;    # maximum number of connections that each worker process can handle simultaneously.
}
```

---

### HTTP Block:

- configuration directives related to HTTP traffic.

```conf
http {
    include       /etc/nginx/mime.types;    # Imports additional configuration files or modules.
    default_type  application/octet-stream; # Sets the default MIME type for responses that lack a Content-Type header.
}
```

---

### Server Blocks (Virtual Hosts)

- settings for specific websites or applications.

```conf
server {
    listen 80;  # Specifies the IP address and port on which Nginx will listen for incoming connections.
    server_name example.com;    # Defines the domain name associated with the server block.

    location / {
        root /var/www/example.com/html;
        index index.html index.htm;
    }

    # Other server configurations
}
```

---

### Location Blocks

- Specifies how Nginx should handle requests for specific URLs.

```conf

location / {    # Matches requests based on the URI path.
    root /var/www/example.com/html;     # Defines the root directory from which files will be served for this location.
    index index.html index.htm;     # Specifies the default files that Nginx should look for when a directory is requested.
}
```

---
