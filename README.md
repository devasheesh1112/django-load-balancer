# Django Load Balancer

A hands-on implementation of load balancing for a Django backend using Nginx as a reverse proxy and load balancer.

## Overview

This project demonstrates how multiple Django backend instances can run behind a single Nginx load balancer.

Instead of sending all requests to a single Django server, Nginx distributes incoming requests across multiple backend instances.

## Architecture

```text
                    Client
                       |
                       v
                 Nginx :8000
                Load Balancer
                       |
          +------------+------------+
          |            |            |
          v            v            v
      Django        Django       Django
       :8001         :8002        :8003
Tech Stack
Python
Django
Nginx
REST API
HTTP
Git & GitHub
Features
Multiple Django backend instances
Nginx reverse proxy
Round-robin load balancing
Backend server identification
Passive failure detection
Backend failure testing
Environment-based server identification
Fault-tolerance demonstration
Project Structure
django-load-balancer/
│
├── api/
│   ├── __init__.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── nginx/
│   └── nginx.conf
│
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
Backend Instances
Backend	Port	Server ID
Django Server 1	8001	8001
Django Server 2	8002	8002
Django Server 3	8003	8003

The SERVER_ID environment variable is used to identify which backend processed a request.

Django API

The main endpoint returns the backend server that handled the request.

Request
GET /
Example Response
{
    "message": "Hello from Django",
    "server": "8001"
}

Another request may be handled by another backend:

{
    "message": "Hello from Django",
    "server": "8002"
}
Nginx Load Balancing

Nginx acts as a reverse proxy and load balancer.

Configuration
worker_processes 1;

events {
    worker_connections 1024;
}

http {

    upstream django_backend {
        server 127.0.0.1:8001 max_fails=3 fail_timeout=10s;
        server 127.0.0.1:8002 max_fails=3 fail_timeout=10s;
        server 127.0.0.1:8003 max_fails=3 fail_timeout=10s;
    }

    server {
        listen 8000;

        location / {
            proxy_pass http://django_backend;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
How Load Balancing Works

The client sends requests to:

http://127.0.0.1:8000/

Nginx receives the request and forwards it to one of the Django backend instances.

The default upstream method is round-robin.

Request 1 → Django :8001
Request 2 → Django :8002
Request 3 → Django :8003
Request 4 → Django :8001
Request 5 → Django :8002
Request 6 → Django :8003

The exact sequence can vary depending on connection behavior.

Testing

You can test the load balancer using curl:

curl http://127.0.0.1:8000/

Example responses:

{
    "message": "Hello from Django",
    "server": "8001"
}
{
    "message": "Hello from Django",
    "server": "8002"
}
{
    "message": "Hello from Django",
    "server": "8003"
}

To generate multiple requests on Windows:

for /L %i in (1,1,12) do @curl -s http://127.0.0.1:8000/ & echo.

Example:

8001
8003
8001
8002
8003
8001
8002
8003
Failure Handling

One of the backend servers can be stopped to test failure handling.

For example:

Django :8001 → Running
Django :8002 → Stopped
Django :8003 → Running

After stopping the 8002 backend, requests can continue through the available backend instances.

                    Nginx :8000
                         |
             +-----------+-----------+
             |                       |
             v                       v
        Django :8001           Django :8003
            ✅                       ✅

                  Django :8002
                       ❌

This demonstrates why multiple backend instances are useful for improving availability.

Failure Detection

The Nginx configuration uses:

max_fails=3
fail_timeout=10s;

For example:

server 127.0.0.1:8001 max_fails=3 fail_timeout=10s;

These settings allow Nginx to passively track unsuccessful upstream requests and temporarily consider a backend unavailable after repeated failures.

Note: This configuration uses passive failure detection. It does not perform continuous active health checks.

How to Run
1. Clone the Repository
git clone https://github.com/devasheesh1112/django-load-balancer.git
cd django-load-balancer
2. Create Virtual Environment
python -m venv venv

Activate on Windows:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Apply Migrations
python manage.py migrate
5. Start Django Backend 1
set SERVER_ID=8001
python manage.py runserver 8001
6. Start Django Backend 2

Open another terminal:

set SERVER_ID=8002
python manage.py runserver 8002
7. Start Django Backend 3

Open another terminal:

set SERVER_ID=8003
python manage.py runserver 8003
8. Start Nginx

Test the Nginx configuration:

nginx.exe -t

If the configuration is valid:

nginx.exe

The load balancer will be available at:

http://127.0.0.1:8000/
Direct Backend Testing

Each backend can also be accessed directly:

http://127.0.0.1:8001/
http://127.0.0.1:8002/
http://127.0.0.1:8003/

Expected server IDs:

8001 → server: 8001
8002 → server: 8002
8003 → server: 8003
Key Concepts
Reverse Proxy
Load Balancing
Round-Robin Load Balancing
Multiple Backend Instances
Nginx Upstream Servers
HTTP Request Routing
Environment Variables
Passive Failure Detection
Fault Tolerance
Backend Scalability
What I Learned

Through this project, I learned how a reverse proxy can sit in front of multiple backend servers and distribute incoming traffic between them.

I also implemented and tested multiple Django instances behind Nginx and verified how requests are distributed across backend servers.

The failure test helped me understand how multiple backend instances can improve availability when one backend becomes unavailable.

Future Improvements
Dockerize the backend services
Add PostgreSQL
Add Redis caching
Add Celery for background tasks
Add application health checks
Add monitoring and logging
Deploy the architecture to a cloud environment
Author

Devasheesh Patidar

GitHub: https://github.com/devasheesh1112
