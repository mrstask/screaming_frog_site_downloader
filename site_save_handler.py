import aiohttp
import asyncio
import time

from page_handler import write_binary
from result_parser import open_file


qu = asyncio.Queue()


async def start_saving_process(urls, domain: str):
    for url in urls:
        await qu.put(url)
    tasks = []
    for _ in range(1):
        task = asyncio.Task(worker(qu, domain))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def worker(queue, domain: str):
    async with aiohttp.ClientSession() as session:
        while queue.qsize() > 0:
            url = await queue.get()
            try:
                async with session.get(url, allow_redirects=False, verify_ssl=False) as response:
                    await write_binary(response, domain)
            except Exception as e:
                print('session get exception for url', url, type(e), e)