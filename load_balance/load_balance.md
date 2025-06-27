# Nginx - Web Server

[Back](../README.md)

- [Nginx - Web Server](#nginx---web-server)
  - [Load Balancing](#load-balancing)
  - [Lab: Round Robin with Weigh](#lab-round-robin-with-weigh)

---

## Load Balancing

- Load Balancing Method
  - default: `Round Robin`

| Method                 | DESC                                                                         | Example                            |
| ---------------------- | ---------------------------------------------------------------------------- | ---------------------------------- |
| Round Robin            | distributed evenly across the servers                                        |                                    |
| Least Connections      | with the least number of active connections                                  | `least_conn;`                      |
| IP Hash                | determined by the client IP address, same client(ip) gets same server        | `ip_hash;`                         |
| Generic Hash           | determined from a user‑defined key.                                          | `hash $request_uri consistent;`    |
| Least Time(NGINX Plus) | with the lowest average latency and the lowest number of active connections. | `least_time header;`               |
| Random (NGINX Plus)    | passed to a randomly selected server.                                        | `random two least_time=last_byte;` |

- Consideration: Server Weights
  - Used by Round Robin, Least Connections, and Random
  - weight parameter:
    - default weight: `1`
    - `server backend1.example.com weight=5;`

---

## Lab: Round Robin with Weigh

```conf
events{}

http {

    upstream backend {
        server app01:8000 weight=4;
        server app02:8000;
    }

    server {
        listen 8080;
        server_name localhost;

        # reverse proxy
        location / {
            proxy_pass http://backend;
        }
    }
}
```
