# Nginx - Common Command

[Back](../README.md)

- [Nginx - Common Command](#nginx---common-command)
  - [Control Nginx Service](#control-nginx-service)
  - [Control NGINX Processes at Runtime](#control-nginx-processes-at-runtime)

---

## Control Nginx Service

| CMD                       | DESC                                        |
| ------------------------- | ------------------------------------------- |
| `systemctl status nginx`  | View Nginx status                           |
| `systemctl start nginx`   | Start Nginx                                 |
| `systemctl stop nginx`    | Stop Nginx                                  |
| `systemctl restart nginx` | Restart Nginx                               |
| `systemctl reload nginx`  | Reload Nginx (without dropping connections) |
| `systemctl enable nginx`  | Enable Nginx to start on boot               |
| `systemctl disable nginx` | Disable automatic start of Nginx on boot    |

## Control NGINX Processes at Runtime

Master and Worker Processes

- `NGINX` has **one** `master process` and **one or more** `worker processes`.

  - If caching is enabled, the `cache loader` and `cache manager processes` also run at startup.

- `master process`:

  - used to read and evaluate configuration files, as well as maintain the worker processes.

- `worker processes`:
  - do the actual processing of requests.
  - NGINX relies on **OS-dependent mechanisms** to efficiently **distribute requests** among worker processes.
- `worker_processes` directive:
  - used to define the number of `worker processes`
  - can either be set to a **fixed** number or configured to **adjust automatically** to the number of available **CPU cores**.

---

| CMD                         | DESC                                  |
| --------------------------- | ------------------------------------- |
| `nginx -t`                  | Check Nginx configuration syntax      |
| `nginx -v`                  | Check Nginx version                   |
| `nginx -s quit`             | Graceful shutdown                     |
| `nginx -s stop`             | Force shutdown                        |
| `sudo systemctl kill nginx` | Force stop if graceful shutdown fails |
| `nginx -s reload`           | Reload the cf                         |
| `nginx -s reopen`           | Reopen the log file                   |
| `ps -ax \| grep nginx`      | Show process                          |
