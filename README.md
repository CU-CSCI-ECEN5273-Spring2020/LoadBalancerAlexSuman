# Load Balancer

## Requirements

The load balancer requires at least Python 3.7 to run. The server requires Python 3 or higher.

## Running as a service

Both the load balancer and the testing server can be run as services. This can be done using the following commands on GCP:

### Load Balancer:
``` sh
python3.7 balancer_service.py start       # Start the service
python3.7 balancer_service.py stop        # Stop the service
python3.7 balancer_service.py restart     # Restart the service
```

### Server:
``` sh
python3 intensive_server_service.py start       # Start the service
python3 intensive_server_service.py stop        # Stop the service
python3 intensive_server_service.py restart     # Restart the service
```