import re
import pandas as pd
import matplotlib.pyplot as plt
import asyncio
import aiohttp


async def send_request(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    url = "http://127.0.0.1:5555/home"  # Load balancer URL
    num_requests = 10000

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url) for _ in range(num_requests)]
        await asyncio.gather(*tasks)


def analyze_logs(log_files):
    server_counts = {}
    for log_file in log_files:
        with open(log_file, 'r') as f:
            for line in f:
                match = re.search(r"Server ID: (s\d+)", line)
                if match:
                    server_id = match.group(1)
                    server_counts[server_id] = server_counts.get(server_id, 0) + 1

    return server_counts


def visualize_results(server_counts):
    df = pd.DataFrame.from_dict(server_counts, orient='index', columns=['Request Count'])
    df.plot(kind='line', marker='o')
    plt.title('Load Balancer Request Distribution')
    plt.xlabel('Server ID')
    plt.ylabel('Request Count')
    plt.grid(axis='y', linestyle='--')
    plt.show()


if __name__ == "__main__":
    asyncio.run(main())
    log_files = [
        'server_logs/s10159.log',
        'server_logs/s147047.log',
        'server_logs/s622449.log'
    ]
    server_counts = analyze_logs(log_files)
    visualize_results(server_counts)
