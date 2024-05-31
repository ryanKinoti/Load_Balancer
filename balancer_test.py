import asyncio
import aiohttp


async def send_request(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []

        for _ in range(10000):
            tasks.append(asyncio.ensure_future(send_request(session, "http://127.0.0.1:5555/home")))
        responses = await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
