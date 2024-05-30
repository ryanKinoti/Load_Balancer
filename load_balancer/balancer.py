from flask import Flask, jsonify, request, redirect
from sortedcontainers import SortedDict

from hashing import ConsistentHashing

app = Flask(__name__)
consistent_hash = ConsistentHashing()
registered_paths = {'/home', '/heartbeat'}


@app.route('/')
def root():
    return redirect('/<path>')


@app.route('/rep', methods=['GET'])
def get_replicas():
    # Returns the status of the replicas managed by the load balancer
    status = {}
    try:
        for server_hash, server_tuple in consistent_hash.hash_ring.items():
            server_key = f"{server_tuple[0]} ({server_tuple[1]})"  # Convert tuple to string
            if server_key not in status:
                status[server_key] = []
            status[server_key].append(server_hash)
        return jsonify(message={"N": len(status), "replicas": status}, status="successful"), 200
    except Exception as e:
        return jsonify(message={"error": str(e)}, status="failure"), 500


@app.route('/add', methods=['POST'])
def add_servers():
    data = request.get_json()
    n = data['n']
    server_ids = data['server_ids']
    hostnames = data['hostnames']

    if len(server_ids) != n:
        return jsonify(message={"error": "Mismatch between number of servers and number of hostnames"}), 400
    else:
        if len(hostnames) < n:
            default_hostname_prefix = "unnamed_"
            for i in range(len(hostnames), n):
                hostnames.append(f"{default_hostname_prefix}{i}")
        for server_id in server_ids:
            consistent_hash.add_server_to_ring(server_id, hostnames.pop(0))

        return jsonify(message={"Added servers": n, "total_servers": consistent_hash.no_of_servers},
                       status="successful"), 200


@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.get_json()
    n = data['n']
    hostnames = data['hostnames']

    if len(hostnames) != n:
        return jsonify(message={"error": "Mismatch between count 'n' and the actual list of hostnames provided"},
                       status="failure"), 400

    results = []
    for hostname in hostnames:
        result, status_code = consistent_hash.remove_server_from_ring(hostname)
        results.append(result)
        if status_code != 200:
            break

    if all(result['status'] == 'successful' for result in results):
        return jsonify(message={"N": len(consistent_hash.hash_ring), "results": results}, status="successful"), 200
    else:
        # If any hostname failed to remove, return the error from the first failed attempt
        first_failure = next((res for res in results if res['status'] == 'failure'), None)
        return jsonify(first_failure), 400


@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    print(f"Path: {path}")
    server_id = consistent_hash.map_request_to_server(hash(path))
    return jsonify(message=f"Request {path} routed to Server {server_id}"), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)
