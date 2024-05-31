### Customizable Load Balancer

This project implements a customizable load balancer using consistent hashing to distribute incoming requests across multiple server replicas. The load balancer ensures even load distribution, scalability, and fault tolerance in a distributed system.

#### Project Structure

*   **`server/`**: Contains the code for the server replicas.
    *   **`Dockerfile`**: Builds the Docker image for the server replicas.
    *   **`server.py`**: Implements the server logic, including endpoints for handling requests and heartbeats.
*   **`load_balancer/`**: Contains the code for the load balancer.
    *   **`Dockerfile`**: Builds the Docker image for the load balancer.
    *   **`balancer.py`**: Implements the load balancer logic, including consistent hashing, request routing, and server management.
    *   **`hashing.py`**: Implements the consistent hashing algorithm.
*   **`docker-compose.yml`**: Defines the Docker services for the load balancer and server replicas.

#### Consistent Hashing

The load balancer utilizes consistent hashing to map requests and servers to a circular hash ring. Each server is represented by multiple virtual nodes to ensure better load distribution. The consistent hashing algorithm is implemented in `hashing.py`.

#### Load Balancer Functionality

The load balancer provides the following functionalities:

*   **Request Routing**: Distributes incoming requests to the appropriate server replica based on the consistent hashing algorithm.
*   **Server Management**: Adds and removes server replicas dynamically to handle scaling up or down.
*   **Fault Tolerance**: Detects server failures and redistributes the load to maintain system availability.
*   **Monitoring**: Provides endpoints to monitor the status of server replicas.

#### Usage

1.  **Build and Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images for the load balancer and server replicas and start the containers.

2.  **Access Load Balancer Endpoints**:
    The load balancer will be accessible at `http://localhost:5555`. You can use the following endpoints:
    *   **`GET /rep`**: Get the status of server replicas.
    *   **`POST /add`**: Add new server replicas.
    *   **`DELETE /rm`**: Remove server replicas.
    *   **`GET /<path>`**: Route requests to the appropriate server replica.

#### Configuration

You can customize the load balancer's behavior by modifying the following parameters in `hashing.py`:

*   **`slots`**: The number of slots in the hash ring.
*   **`no_of_servers`**: The initial number of server replicas.

#### Assumptions

*   The server replicas are stateless and can handle requests independently.
*   The client requests have unique identifiers.
*   The load balancer has sufficient resources to manage the server replicas.

#### Testing and Performance Analysis

The load balancer has been tested with various scenarios, including adding and removing servers, simulating server failures, and measuring request distribution. The results demonstrate that the load balancer effectively distributes the load evenly across the server replicas and recovers from failures promptly.

#### Future Improvements

*   Implement a more sophisticated load balancing algorithm, such as weighted consistent hashing or least connections.
*   Add support for session persistence to ensure that requests from the same client are routed to the same server.
*   Integrate with a service discovery mechanism to automatically discover and manage server replicas.

Please refer to the code documentation and comments for more details on the implementation.