# Nginx - Troubleshooting

[Back](../README.md)

- [Nginx - Troubleshooting](#nginx---troubleshooting)
  - [Testing and troubleshooting](#testing-and-troubleshooting)
  - [Log analysis](#log-analysis)
  - [Port Debugging](#port-debugging)
  - [Force nginx to stop](#force-nginx-to-stop)

---

## Testing and troubleshooting

```sh
# Test website response
curl -I http://localhost        # Fetch the HTTP headers only
curl -v http://localhost        # get verbose

# get status
sudo systemctl status nginx

# Locate the cf in use
nginx -t 2>&1 | grep "configuration file"
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test failed

sudo nginx -t       # Test cf syntax
sudo nginx -T       # Test and show cf details

nginx -V 2>&1 | grep -o with-[a-z_]*            # List all loaded modules
```

---

## Log analysis

```sh
# locate log file
sudo nginx -T | grep log
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
# error_log /var/log/nginx/error.log;
#         access_log /var/log/nginx/access.log;

# locate error log
nginx -V 2>&1 | awk -F: '/configure arguments/ {print $2}' | xargs -n1 | grep 'error-log-path'
# --error-log-path=stderr

# locate access log
nginx -V 2>&1 | awk -F: '/configure arguments/ {print $2}' | xargs -n1 | grep 'http-log-path'
# --http-log-path=/var/log/nginx/access.log

sudo tail -f /var/log/nginx/error.log       # view error
sudo tail -n 50 /var/log/nginx/error.log

sudo tail -f /var/log/nginx/access.log      # view accesslog

# Search for specific errors
sudo grep "error" /var/log/nginx/error.log
sudo grep "404" /var/log/nginx/access.log

# Check if there are any binding errors
sudo journalctl -u nginx -n 20
```

---

## Port Debugging

- Test if Nginx is running and listening on ports:

```sh
# sudo netstat -tlnp | grep nginx
sudo ss -tlnp | grep nginx
# tcp   LISTEN 0      511          0.0.0.0:http        0.0.0.0:*    users:(("nginx",pid=4108,fd=5),("nginx",pid=4107,fd=5),("nginx",pid=4106,fd=5),("nginx",pid=4105,fd=5),("nginx",pid=4102,fd=5))
# tcp   LISTEN 0      511             [::]:http           [::]:*    users:(("nginx",pid=4108,fd=6),("nginx",pid=4107,fd=6),("nginx",pid=4106,fd=6),("nginx",pid=4105,fd=6),("nginx",pid=4102,fd=6))

# Check if ports 80/443 are occupied
sudo lsof -i :80
# COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
# nginx   4102     root    5u  IPv4  34134      0t0  TCP *:http (LISTEN)
# nginx   4102     root    6u  IPv6  34135      0t0  TCP *:http (LISTEN)
# nginx   4105 www-data    5u  IPv4  34134      0t0  TCP *:http (LISTEN)
# nginx   4105 www-data    6u  IPv6  34135      0t0  TCP *:http (LISTEN)
# nginx   4106 www-data    5u  IPv4  34134      0t0  TCP *:http (LISTEN)
# nginx   4106 www-data    6u  IPv6  34135      0t0  TCP *:http (LISTEN)
# nginx   4107 www-data    5u  IPv4  34134      0t0  TCP *:http (LISTEN)
# nginx   4107 www-data    6u  IPv6  34135      0t0  TCP *:http (LISTEN)
# nginx   4108 www-data    5u  IPv4  34134      0t0  TCP *:http (LISTEN)
# nginx   4108 www-data    6u  IPv6  34135      0t0  TCP *:http (LISTEN)
sudo lsof -i :443

# Count real-time connections
sudo netstat -an | grep :80 | wc -l
sudo ss -an | grep :80 | wc -l
# 4
```

---

## Force nginx to stop

```sh
# Graceful shutdown
sudo systemctl stop nginx
# sudo nginx -s quit  # equivalent

# Force stop if graceful shutdown fails
sudo systemctl kill nginx
sudo nginx -s stop

# If the above methods don't work, you can manually kill the processes:
ps aux | grep nginx     # identify nginx process

sudo kill PID       # Kill by process ID
sudo kill -9 PID    # Force kill if regular kill doesn't work
sudo pkill nginx    # Kill all nginx processes at once
sudo pkill -9 nginx # Force kill all nginx processes

# Check if nginx is really stopped
ps aux | grep nginx

# Check if ports 80/443 are still in use
sudo ss -tlnp | grep :80
sudo ss -tlnp | grep :443

# After fixing issue, restart nginx
sudo systemctl start nginx
```

---
