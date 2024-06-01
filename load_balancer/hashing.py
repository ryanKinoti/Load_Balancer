import hashlib
import math

import docker
from sortedcontainers import SortedDict


class ConsistentHashing:

    def __init__(self, slots=512, no_of_servers=3):
        self.no_of_servers = no_of_servers
        self.slots = slots
        self.virtual_servers = int(math.log2(slots))
        self.hash_ring = SortedDict()
        self.registered_paths = {'home', 'heartbeat', 'server_status'}
        self.init_servers()
        self.server_hash_map = {}

    # j => is the number of virtual servers per server
    # Hash function to map requests to slots
    def request_hash_fn(self, i):
        # return int(hashlib.md5(str(i).encode()).hexdigest(), 16) % self.slots
        # value = (i + (2 * i) + 17) // 2
        value = (i ** 2 + 2 * (i ** 2) + 17 ** 2)
        hash_value = value % self.slots
        return hash_value

    # Hash function to map virtual servers to slots
    def virtual_hashing(self, server_id, virtual_index):
        # key = f"{server_id}-{virtual_index}"
        # return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.slots
        numeric_id = int(server_id[1:])
        j = virtual_index
        value = numeric_id + j + (2 * j) + 25
        hash_value = value % self.slots
        return hash_value

    # Add server to the hash ring
    def add_server_to_ring(self, server_id, hostname):
        if server_id in [value[0] for value in self.hash_ring.values()]:

            for key, value in self.hash_ring.items():
                if value[0] == server_id:
                    self.hash_ring[key] = (server_id, hostname)
                    print(f"Updated server {server_id} with hostname {hostname}")
                    break
            raise ValueError(f"Server ID '{server_id}' already exists in the hash ring")

        else:
            for i in range(self.virtual_servers):
                server_hash_value = self.virtual_hashing(server_id, i)
                self.hash_ring[server_hash_value] = (server_id, hostname)
            self.no_of_servers += 1
            print(f"Added server {server_id} with hostname {hostname}")

    # Remove server from the hash ring
    def remove_server_from_ring(self, hostname):
        server_id = None
        for key, value in self.hash_ring.items():
            if value[1] == hostname:
                server_id = value[0]
                break
        if server_id is None:
            return {"message": f"Error: Server with hostname {hostname} not found or may have been removed",
                    "status": "failure"}, 404

        to_remove = [slot for slot, value in self.hash_ring.items() if value[0] == server_id]
        for slot in to_remove:
            del self.hash_ring[slot]

        return {"message": f"Server {hostname} removed successfully", "status": "successful"}, 200

    # Get the server for a given request
    def map_request_to_server(self, request_id):
        request_hash_value = self.request_hash_fn(request_id)
        # Find the server with the next highest hash value
        for server_hash, server_id in self.hash_ring.items():
            if server_hash >= request_hash_value:
                return server_id
        # If the request hash value is greater than all server hash values wrap around to the first server
        return self.hash_ring.peekitem(0)[1]

    # in case a server does not respond to heartbeat and needs to be updated
    def update_servers(self, server_id, hostname):
        self.remove_server_from_ring(server_id)
        self.add_server_to_ring(server_id, hostname)
        return self.hash_ring

    # initiating default servers
    def init_servers(self):
        try:
            client = docker.from_env()  # Connect to the Docker daemon
            containers = client.containers.list(filters={"name": "server"})  # Get server containers

            for container in containers:
                env_vars = container.attrs['Config']['Env']  # Get container's environment variables
                server_id = next((var.split('=')[1] for var in env_vars if var.startswith('SERVER_ID=')), None)
                if server_id:
                    self.add_server_to_ring(server_id, container.name)  # Add to hash ring

        except docker.errors.APIError as e:
            print(f"Error communicating with Docker daemon: {e}")
